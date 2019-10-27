<template>
<div class="row itemRow">
    <div class="col-12 text-left" @click="handleClick">
        <div class="row">
            <div class="col-12">
                <h3>{{item.name}}</h3>
            </div>
        </div>
        <div class="row">
            <div class="col-8">
                Available
            </div>
            <div class="col-4">
                {{item.q}} kg
            </div>
        </div>
    </div>
    <div class="col-12" v-if="this.clicked">
        <div class="form-group">
            <input id="amount" type="number" class="form-control" v-model="amount">
            <button ref="pickButton" class="btn btn-pirates" @click="pickSingleItem">Add item</button>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: 'ItemRow',
    props: ['item'],
    data() {
        return {
            clicked: false,
            amount: 0,
        };
    },
    methods: {
        handleClick() {
            this.clicked = !this.clicked;
        },
        pickSingleItem() {
          let getAmount = parseInt(this.amount);
            if (getAmount) {
                this.$store.commit('addItems', [{
                    id: this.item['id'],
                    q: getAmount
                }, ]);
                this.item.q -= getAmount;
            }
        },
    },
};
</script>

<style scoped>
.itemRow {
    text-align: center;
    border-bottom: 1px solid #434a52;

}

.itemRow h3 {
    font-size: 16px;
    color: #F07A56;
    text-transform: uppercase;
    font-weight: 600;
    margin: 0;
}
</style>
