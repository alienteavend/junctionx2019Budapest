import datetime
import random
import typing
from threading import Timer
import json

USER_TYPE_SHOP_MANAGER = 1
USER_TYPE_PARTNER = 2

PICK_DURATION_LIMIT_MINS =  1
RECIPE_MATCH_TRESHOLD = 0.75


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Ingredient):
            return {
                'id' : o.id,
                'name' : o.name
            }
        return CustomEncoder(self, o)

class IngredientToIdEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Ingredient):
            return o.id
        return IngredientToIdEncoder(self, o)


class Ingredient:
    def __init__(self, barcode: str, name: str, avgPricePerUnit: float):
        self.id: int = MemDB.getNextId()
        self.barCode: str = barcode
        self.name: str = name
        self.avgPricePerUnit: float = avgPricePerUnit


class Recipe:
    def __init__(self, name, min, max, ingredients):
        self.id: int = MemDB.getNextId()
        self.name = name
        self.minPortions = min
        self.maxPortions = max
        self.ingredients: typing.Dict[Ingredient, float] = ingredients

class Partner:
    def __init__(self, name: str, email: str):
        self.id: int = MemDB.getNextId()
        self.name: str = name
        self.email: str = email
        self.recipes: [Recipe] = []

class Shop:
    def __init__(self, managerEmail: str):
        self.id = MemDB.getNextId()
        self.managerEmail: str = managerEmail
        self.partners: [Partner] = []
        self.mainPartner: Partner = None

class Draft:
    STATUS_INITIALIZING = 0
    STATUS_STARTED = 1
    STATUS_FINISHED = 2

    def __init__(self, shop, delegate):
        self.id = MemDB.getNextId()
        self.shop = shop
        self.partners: [Partner] = None
        self.availableDonations: typing.Dict[Ingredient, float] = {}
        self.partnerPicks: typing.Dict[Partner, typing.Dict[Ingredient, float]] = None

        self.pickingPartnerIndex: int = 0
        self.pickDeadline: datetime.datetime = None

        self.status: int = Draft.STATUS_INITIALIZING
        self.timer: Timer = None

        self.delegate = delegate

        self._initPartners()

    def _initPartners(self):
        self.partners = [x for x in self.shop.partners]
        random.shuffle(self.partners)

        self.partnerPicks = {}
        for p in self.partners:
            self.partnerPicks[p] = {}

        self.pickingPartnerIndex = 0

    def addIngredient(self, ingredient: Ingredient, quantity: float):
        assert self.status is Draft.STATUS_INITIALIZING, "adding ingredients is forbidden after a draft has been started"
        donation = self.availableDonations.get(ingredient, None)
        if donation is not None:
            self.availableDonations[ingredient] += quantity
        else:
            self.availableDonations[ingredient] = quantity

    def pickIngredients(self, partner: Partner, ingredients: typing.Dict[Ingredient, float]):
        self._assertCanPick(partner)
        for ingredient, quantity in ingredients.items():
            self._pickIngredient(partner, ingredient, quantity)
        self._finishRound()

    def _pickIngredient(self, partner: Partner, ingredient: Ingredient, quantity: float):
        avalQuantity = self.availableDonations.get(ingredient, None)
        assert avalQuantity >= quantity, "You cannot pick this amount of food"
        self.availableDonations[ingredient] -= quantity
        if self.availableDonations[ingredient] <= 0:
            self.availableDonations.pop(ingredient, None)

        picks = self.partnerPicks[partner]
        assert picks is not None

        donation = picks.get(ingredient, None)
        if donation is not None:
            picks[ingredient] += quantity
        else:
            picks[ingredient] = quantity

    def _finishDraft(self):
        self.status = Draft.STATUS_FINISHED
        self.timer = None
        if self.delegate is not None:
            self.delegate.onFinish(self)

    def _shouldFinish(self) -> bool:
        return len(self.joinedPartners) == 0 \
               or len(self.availableDonations) == 0 \
               or datetime.datetime.now() > self.endTime

    def _incPickingIndex(self):
        self.pickingPartnerIndex = (self.pickingPartnerIndex + 1) % len(self.partners)

    def pickingPartner(self) -> Partner:
        if self.status != Draft.STATUS_STARTED:
            return None
        return self.partners[self.pickingPartnerIndex]

    def _assertCanPick(self, partner: Partner):
        assert partner == self.pickingPartner(), "only the active partner can pick stuff"

    # todo: refactor: move these methods into an other class ~ DraftScheduler
    def start(self):
        self.status = Draft.STATUS_STARTED
        self.pickingPartnerIndex = -1 # _startNextRound will auto inc this
        self._startNextRound()

    def _startNextRound(self):
        self.pickingPartnerIndex = self.chooseNextPartnerIndex(self.pickingPartnerIndex + 1)
        if self.pickingPartnerIndex is None:
            self._finishDraft()
            return

        partner = self.partners[self.pickingPartnerIndex]
        if self.delegate is not None:
            self.delegate.onNextRound(self, partner)

        self.pickDeadline = datetime.datetime.now() + datetime.timedelta(minutes=PICK_DURATION_LIMIT_MINS)
        self.timer = Timer(PICK_DURATION_LIMIT_MINS * 60, self._startNextRound)
        self.timer.start()

    def _finishRound(self):
        self.timer.cancel()
        self.timer = None
        self._startNextRound()

    def chooseNextPartnerIndex(self, startIndex) -> int:
        for index in range(startIndex, len(self.partners)):
            p = self.partners[index]
            if len(self.matchingRecipes(p)) > 0:
                return index
        return None

    def matchingRecipes(self, p: Partner) -> [Recipe]:
        result: [Recipe] = []
        for r in p.recipes:
            match = ingredientsRecipeMatch(self.availableDonations, r)
            if match >= RECIPE_MATCH_TRESHOLD:
                result.append(r)
        return result


def ingredientsRecipeMatch(ingredients: typing.Dict[Ingredient, float], recipe: Recipe) -> float:
    minPortions = recipe.minPortions
    sumPrice = 0.0
    missingPrice = 0.0
    for ri, q in recipe.ingredients.items():
        minQuantity = q * minPortions
        sumPrice += ri.avgPricePerUnit * minQuantity

        available = ingredients.get(ri, 0)
        missingPrice += abs(min(0, available - minQuantity)) * ri.avgPricePerUnit

    missingPtg = missingPrice / sumPrice
    return 1.0 - missingPtg


class MemDB:
    NEXT_ID = 1
    @staticmethod
    def getNextId() -> int:
        id = MemDB.NEXT_ID
        MemDB.NEXT_ID += 1
        return id

    INGREDIENTS: [Ingredient] = []
    SHOPS: [Shop] = []
    PARTNERS: [Partner] = []
    DRAFTS: [Draft] = []

    @staticmethod
    def getDraft(id) -> Draft:
        for draft in MemDB.DRAFTS:
            if draft.id == id:
                return draft
        return None

    @staticmethod
    def getIngredient(id) -> Ingredient:
        for i in MemDB.INGREDIENTS:
            if i.id == id:
                return i
        return None

    @staticmethod
    def getPartner(id) -> Partner:
        for p in MemDB.PARTNERS:
            if p.id == id:
                return p
        return None

    @staticmethod
    def init():
        partner1 = Partner("kifozde", "qwerjoe@gmail.com")
        partner2 = Partner("fozelekfalo", "qwerjoe@gmail.com")
        partner3 = Partner("bozsineni", "qwerjoe@gmail.com")
        partner4 = Partner("egyeee", "qwerjoe@gmail.com")
        mainPartner = Partner("voroskereszt", "qwerjoe@gmail.com")

        MemDB.PARTNERS = [
            partner1,
            partner2,
            partner3,
            partner4,
            mainPartner
        ]

        shop = Shop("qwerjoe@gmail.com")
        shop.partners = [
            partner1,
            partner2,
            partner3,
            partner4
        ]
        shop.mainPartner = mainPartner

        MemDB.SHOPS = [shop]

        alma = Ingredient("123-456-1", "alma", 400)
        csirke = Ingredient("123-456-2", "csirke", 1600)
        sajt = Ingredient("123-456-3", "sajt", 2500)
        krumpli = Ingredient("123-456-4", "krumpli", 300)
        kolbasz = Ingredient("123-456-5", "kolbasz", 3500)
        hagyma = Ingredient("123-456-6", "hagyma", 230)
        tejfol = Ingredient("123-456-7", "tejfol", 1200)
        ananasz = Ingredient("123-456-8", "ananasz", 1400)
        diszno = Ingredient("123-456-9", "diszno", 1400)
        paprika = Ingredient("123-456-10", "paprika", 500)
        paradicsom = Ingredient("123-456-11", "paradicsom", 800)
        olaj = Ingredient("123-456-12", "olaj", 600)

        MemDB.INGREDIENTS = [
            alma,
            csirke,
            sajt,
            krumpli,
            kolbasz,
            hagyma,
            tejfol,
            ananasz,
            diszno,
            paprika,
            paradicsom,
            olaj
        ]

        partner1.recipes = [
            Recipe("lecso", 20, 50,
                   {
                       paradicsom: 0.15,
                       paprika: 0.3,
                       olaj: 0.02,
                       kolbasz: 0.1
                   }),
            Recipe("paprikas krumpli", 20, 50,
                   {
                       krumpli: 0.4,
                       paprika: 0.05,
                       olaj: 0.02,
                       kolbasz: 0.1
                   }),
        ]

        partner2.recipes = [
            Recipe("lecso", 40, 100,
                   {
                       paradicsom: 0.15,
                       paprika: 0.3,
                       olaj: 0.02,
                   }),
            Recipe("paprikas krumpli", 40, 100,
                   {
                       krumpli: 0.4,
                       paprika: 0.05,
                       olaj: 0.02,
                       kolbasz: 0.1
                   }),
        ]

        partner3.recipes = [
            Recipe("ananaszos csirke - krumplipurevel", 20, 50,
                   {
                       csirke: 0.25,
                       ananasz: 0.1,
                       sajt: 0.05,
                       krumpli: 0.3
                   }),
            Recipe("csirke paprikas", 20, 40,
                   {
                       csirke: 0.2,
                       paprika: 0.1,
                       paradicsom: 0.05,
                       olaj: 0.02
                   })
        ]

        partner4.recipes = [
            Recipe("olajos hagyma", 20, 50,
                   {
                       olaj: 0.1,
                       hagyma: 0.3
                   })
        ]

        draft = Draft(shop, None)
        MemDB.DRAFTS = [
            draft
        ]

        print("draft-id: " + str(draft.id))
        draft.addIngredient(csirke, 20)
        draft.addIngredient(krumpli, 5)
        draft.addIngredient(paprika, 30)

        draft.addIngredient(paradicsom, 30)
        draft.addIngredient(krumpli, 45)
        draft.addIngredient(kolbasz, 3)
        draft.addIngredient(hagyma, 10)
        draft.addIngredient(sajt, 10)

















