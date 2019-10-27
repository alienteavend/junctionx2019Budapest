<template>
<div class="row foodrow">
    <div class="col-2 imagecol">
        IMAGE
    </div>
    <div class="col-10 text-left">
        <div class="row">
            <div class="col-12">
                <h3>{{item.name}}</h3>
            </div>
        </div>
        <div class="row">
            <div class="col-8">
                Need
            </div>
            <div class="col-4">
                {{portions * item.q}} kg
            </div>
        </div>
        <div class="row">
            <div class="col-8">
                Get for free
            </div>
            <div class="col-4">
                {{calcGetForFree(item)}} kg
            </div>
        </div>
        <div class="row">
            <div class="col-8">
                Need to buy
            </div>
            <div class="col-4">
                {{calcNeedToBuy(item)}} kg
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
  name: 'FoodRow',
  props: ['item', 'inventory', 'portions'],
  methods: {
    calcGetForFree(item) {
      let obj = this.inventory.find(o => o.name === item.name);
      if(!obj)
        return 0;
      return Math.min(obj.q, this.portions * this.item.q);
    },
    calcNeedToBuy(item) {
      let need = this.portions * item.q;
      let free = this.calcGetForFree(item);
      return need - free;
    },
  },
  created() {
    console.log(this.portions);
  }
};
</script>

<style scoped>
.foodrow {
    text-align: center;
    border-bottom: 1px solid #434a52;

}

.foodrow table th,
.foodrow table td {
    border: none;
    text-align: left;
    color: #cccccc;
    line-height: 10px
}

.foodrow table th {
    text-align: left;

}

.foodrow h3 {
    font-size: 16px;
    color: #F07A56;
    text-transform: uppercase;
    font-weight: 600;
    margin: 0;
}

.imagecol {
    width: 150px;
    height: 150px;
}
</style>
