import os
import json

from flask import Blueprint, jsonify, request
from project.api.models import *

draft_blueprint = Blueprint('draf', __name__)


@draft_blueprint.route('/ingredients', methods=['GET'])
def create_draft():
    return json.dumps(MemDB.INGREDIENTS, cls=CustomEncoder)

# post data:
# {
#   'draft': 12
# }
@draft_blueprint.route('/drafts/start', methods=['POST'])
def start_draft():
    post_data = request.get_json()

    draft_id = post_data['draft']
    draft = MemDB.getDraft(draft_id)
    if draft is None:
        return jsonify({'status': 'error', 'message': 'invalid draft id'})

    draft.start()
    return jsonify({'status': 'ok'})

@draft_blueprint.route('/drafts/info', methods=['POST'])
def draft_info():
    post_data = request.get_json()

    draft_id = post_data['draft']
    draft: Draft = MemDB.getDraft(draft_id)
    if draft is None:
        return jsonify({'status': 'error', 'message': 'invalid draft id'})

    available_array = createAvailableArray(draft)
    picking_id = getPickingId(draft)
    timing_object = createTimingObject(draft)

    response_object = {
        'draft': draft.id,
        'waitingFor': picking_id,
        'timing': timing_object,
        'available': available_array,
        'status': draft.status
    }

    return json.dumps(response_object)

# post data:
# {
#   'draft': 12,
#   'partner': 42,
#   'picks' : [{'id': 0, 'q': 20}, ...]
# }
@draft_blueprint.route('/drafts/pick', methods=['POST'])
def draft_pick():
    post_data = request.get_json()

    draft_id = post_data['draft']
    draft: Draft = MemDB.getDraft(draft_id)
    if draft is None:
        return jsonify({'status': 'error', 'message': 'invalid draft id'})

    partner_id = post_data['partner']
    partner = MemDB.getPartner(partner_id)
    if partner is None:
        return jsonify({'status': 'error', 'message': 'invalid partner id'})

    if partner is not draft.pickingPartner():
        return jsonify({'status': 'error', 'message': 'it\'s not your turn'})

    picked_json = post_data['picks']
    ingredients = {}
    for item in picked_json:
        ingId = item['id']
        ing = MemDB.getIngredient(ingId)
        ingredients[ing] = item['q']

    draft.pickIngredients(partner, ingredients)

    return jsonify({'status': 'ok'})


@draft_blueprint.route('/drafts/partnerInfo', methods=['POST'])
def draft_partner_info():
    post_data = request.get_json()

    draft_id = post_data['draft']
    draft: Draft = MemDB.getDraft(draft_id)
    if draft is None:
        return jsonify({'status': 'error', 'message': 'invalid draft id'})

    partner_id = post_data['partner']
    partner = MemDB.getPartner(partner_id)
    if partner is None:
        return jsonify({'status': 'error', 'message': 'invalid partner id'})

    available_array = createAvailableArray(draft)
    picking_id = getPickingId(draft)
    recipes_array = createRecipesArray(draft.matchingRecipes(partner), draft)
    timing_object = createTimingObject(draft)

    response_object = {
        'draft': draft.id,
        'waitingFor': picking_id,
        'available': available_array,
        'timing': timing_object,
        'status': draft.status,
        'recipes': recipes_array
    }

    return json.dumps(response_object)

def createAvailableArray(draft: Draft):
    return ingredientsMapToArray(draft.availableDonations)

def createRecipesArray(recipes: [Recipe], draft: Draft):
    recipes_array = []
    for recipe in recipes:
        recipes_array.append(createRecipeObject(recipe, ingredientsRecipeMatch(draft.availableDonations, recipe)))
    return recipes_array

def createRecipeObject(recipe: Recipe, matchRatio: float):
    ingredients = ingredientsMapToArray(recipe.ingredients)
    return {
        'name': recipe.name,
        'minPortions': recipe.minPortions,
        'maxPortions': recipe.maxPortions,
        'ingredients': ingredients,
        'match': matchRatio
    }

def ingredientsMapToArray(ingredients: typing.Dict[Ingredient, float]):
    ingredients_array = []
    for k, v in ingredients.items():
        ingredients_array.append({'id': k.id, 'name': k.name, 'q': v})
    return ingredients_array

def createTimingObject(draft: Draft):
    if draft.status != Draft.STATUS_STARTED:
        return None
    return {
        'pickDeadline': draft.pickDeadline.timestamp(),
        'now': datetime.datetime.now().timestamp()
    }

def getPickingId(draft: Draft):
    picking = draft.pickingPartner()
    picking_id = -1
    if picking is not None:
        picking_id = picking.id

    return picking_id
