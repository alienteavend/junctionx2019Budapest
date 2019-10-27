<template>
<div class="slidecontainer">
    <label for="" class="float-left range-label">{{minText}} {{min}}</label>
    <label for="" class="float-right range-label">{{maxText}} {{max}}</label>
    <input type="range" :min="min" :max="max" value="0" class="slider" id="myRange" v-model="value">
</div>
</template>

<script>
export default {
  name: 'Slider',
  props: ['min', 'minText', 'max', 'maxText'],
  data() {
    return {
      value: 0,
    };
  },
  methods: {
  },
};
</script>

<style scoped>
.slidecontainer {
    width: 100%;
    /* Width of the outside container */
}

/* The slider itself */
.slider {
    -webkit-appearance: none;
    /* Override default CSS styles */
    appearance: none;
    width: 100%;
    /* Full-width */
    height: 5px;
    /* Specified height */
    background: -webkit-linear-gradient(left, #F07A56, #A255EB);
    background: -moz-linear-gradient(left, #F07A56, #A255EB);
    background: linear-gradient(to right, #F07A56, #A255EB);
    -webkit-text-fill-color: transparent;
    outline: none;
    /* Remove outline */
    opacity: 0.7;
    /* Set transparency (for mouse-over effects on hover) */
    -webkit-transition: .2s;
    /* 0.2 seconds transition on hover */
    transition: opacity .2s;
}

/* Mouse-over effects */
.slider:hover {
    opacity: 1;
    /* Fully shown on mouse-over */
}

/* The slider handle (use -webkit- (Chrome, Opera, Safari, Edge)
 and -moz- (Firefox) to override default look) */
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    /* Override default look */
    appearance: none;
    width: 10px;
    /* Set a specific slider handle width */
    height: 25px;
    /* Slider handle height */
    background: #fff;
    /* Green background */
    cursor: pointer;
    /* Cursor on hover */
}

.slider::-moz-range-thumb {
    width: 10px;
    /* Set a specific slider handle width */
    height: 25px;
    /* Slider handle height */
    background: #fff;
    /* Green background */
    cursor: pointer;
    /* Cursor on hover */
}

.range-label {
    font-size: 10px;
    color: #fff;
}
</style>
