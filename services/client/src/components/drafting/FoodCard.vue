<template>
<div class="row card mb-3 p-3">
    <div v-if="!clicked">
        <div class="col-12 text-left">
            <div class="row">
                <div class="col-12">
                    <h3 class="item-name" @click="cardClicked">{{recipe.name}}</h3>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    Minimum portions: {{recipe.minPortions}}
                </div>
                <div class="col-12">
                    Maximum portions: {{recipe.maxPortions}}
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <FoodSelectorSlider :value="recipe.match" />
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <div class="col-12 text-left">
            <div class="row">
                <div class="col-12">
                    <h3 @click="cardClicked">{{recipe.name}}</h3>
                </div>
            </div>
            <template v-for="item in recipe.ingredients" v-key:item.name>
                <FoodRow ref="foodRows" :item="item" :inventory="inventory" :portions="portions" v-bind:key="item.name" />
            </template>
            <div class="row">
                <div class="col-12">
                    <div class="form-group">
                        <label for="portion" class="float-left">Min: {{recipe.minPortions}}</label>
                        <label for="portion" class="float-right">Max: {{recipe.maxPortions}}</label>
                        <input id="portion" type="number" class="form-control" :min="recipe.minPortions" :max="recipe.maxPortions" v-model="portions">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-12 text-center">
                    <button ref="pickButton" class="btn btn-pirates" @click="pickRecipeItems">Add free items</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import FoodRow from './FoodRow';
import Slider from './Slider';
import FoodSelectorSlider from './FoodSelectorSlider';

export default {
    name: 'FoodCard',
    props: ['recipe', 'inventory'],
    components: {
        FoodRow,
        Slider,
        FoodSelectorSlider,
    },
    data() {
        return {
            clicked: false,
            portions: 0,
        };
    },
    methods: {
        cardClicked() {
            this.clicked = !this.clicked;
        },
        pickRecipeItems() {
            for (let i = 0; i < this.$refs.foodRows.length; ++i) {
                let currentRow = this.$refs.foodRows[i];
                let getForFree = currentRow.calcGetForFree(currentRow.item);
                let itemId = currentRow.item["id"];
                if (getForFree) {
                    this.$store.commit('addItems', [{
                        id: itemId,
                        q: getForFree
                    }, ]);
                }
            }
            this.$refs.pickButton.disabled = true;
            this.$refs.pickButton.innerHTML = 'Already picked';
        },
    },
    created() {
        this.portions = this.recipe.maxPortions;
    }

};
</script>

<style scoped>
.item-name {
    font-size: 16px;
    color: #F07A56;
    text-transform: uppercase;
    font-weight: 600;
    margin: 0;
}
</style>
