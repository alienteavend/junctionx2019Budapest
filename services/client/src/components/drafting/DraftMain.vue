<template>
<div class="container">
    <div v-if="!$route.query.partnerKey">
        <div class="row mb-3">
            <div class="col-lg-12 text-center">
                <h2>Partner key is missing</h2>
            </div>
        </div>
    </div>
    <div v-else-if="!draftRunning">
        <div class="row mb-3">
            <div class="col-lg-12 text-center">
                <h2>Waiting for draft</h2>
            </div>
        </div>
    </div>
    <div v-else-if="draftRunning && !amIDrafting">
        <div class="row mb-3">
            <div class="col-lg-12 text-center">
                <h2>Draft ongoing, no items for you</h2>
                Currently drafting: {{this.draft_data.waitingFor}}
            </div>
        </div>
    </div>
    <div v-else-if="draftRunning && amIDrafting">
        <div class="row">
            <div class="col-lg-12">
                <h1>Food drafting</h1>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-lg-12">
                <h2>Available recipes for you</h2>
            </div>
        </div>

        <template v-for="item in recipes" v-key:item.name>
            <FoodCard :recipe="item" :inventory="inventory" v-bind:key="item.name" />
        </template>

        <div class="row mb-3">
            <div class="col-lg-12">
                <h2>Available items</h2>
            </div>
        </div>

        <template v-for="item in inventory" v-key:item.name>
            <ItemRow :item="item" v-bind:key="item.name" />
        </template>

        <div class="row mb-3">
            <div class="col-lg-12">
                <h2>Your items</h2>
            </div>
        </div>

        <template v-for="item in cartItems" v-key:item.id>
            <ItemRow :item="item" v-bind:key="item.name" />
        </template>

        
        <div class="row">
            <div class="col-12 text-center">
                <button ref="finishedButton" class="btn btn-pirates" @click="finishedWithDraft">Finalize picks</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import FoodCard from './FoodCard';
import ItemRow from './ItemRow';
import axios from 'axios';

export default {
    name: 'DraftMain',
    components: {
        FoodCard,
        ItemRow,
    },
    data() {
        return {
            ROOT_API: 'http://localhost:5000/drafts',
            draft_key: 52,
            partnerKey: this.$route.query.partnerKey,
            inventory: [],
            data: null,
            recipes: [],
            draftRunning: false,
            amIDrafting: false,
        };
    },
    computed: {
        cartItems() {
            let cart = this.$store.state.cart;
            let items = [];
            for(let i = 0; i< cart.length; ++i) {
                let item = cart[i];
                let obj = this.inventory.find(o => o.id === item.id);
                obj = Object.assign({}, obj);
                obj.q = item.q;
                items.push(obj);
            }
            return items;
        }
    },
    methods: {
        getDrafts() {
            const path = `${this.ROOT_API}/partnerInfo`;
            axios.post(path, {
                    draft: parseInt(this.draft_key),
                    partner: parseInt(this.partnerKey),
                })
                .then((res) => {
                    this.draft_data = res.data;
                    if(this.draft_data.status == 1) {
                        this.draftRunning = true;
                        this.amIDrafting = this.draft_data.waitingFor === parseInt(this.partnerKey);
                        
                    } else {
                        this.draftRunning = false;
                        this.amIDrafting = false;
                    }
                    this.inventory = res.data.available;
                    this.recipes = res.data.recipes;
                    // eslint-disable-next-line
                    console.error(this.draft_data);
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        finishedWithDraft() {
            const path = `${this.ROOT_API}/pick`;
            axios.post(path, {
                    draft: parseInt(this.draft_key),
                    partner: parseInt(this.partnerKey),
                    picks: this.$store.state.cart,
                })
                .then((res) => {
                    // eslint-disable-next-line
                    console.error('Accepted');
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        pollDrafts() {
        let self = this;
        this.getDrafts();
            setTimeout(function(){
                   console.log("asd");
                   self.pollDrafts();
                }, 1000);
        },
    },
    created() {
        this.pollDrafts();
        
    },
};
</script>
