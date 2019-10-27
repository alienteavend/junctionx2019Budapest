<template>


<div class="progress">
    <div class="progress__container">
        <div class="progress__bar" v-bind:style="{width: parseInt(value*100-((value*100)*0.05))  + '%'}">
            <div class="step"  v-bind:style="{left: parseInt((value*100) -((value*100)*0.1)  ) + '%'}">
                <div class="step__content">
                    <div class="step__title currentProgressTitle">Surplus Value</div>
                    <span class="CurrentProgressIcon"></span>
                    <div class=" currentProgressValue">{{parseInt(value*100)}} match</div>
                </div>
            </div>
            <div class="Endstep" style="left: 95%">
                <div class="step__content">
                    <div class="step__title EndTitle">For 100 plate</div>
                    <span class="EndIcon"></span>
                    <div class=" EndValue">$100</div>
                </div>
            </div>
        </div>
    </div>
</div>


</template>

<script>
export default {
  name: 'FoodSelectorSlider',
  props: ['value'],
  created() {
      console.log(this.value);
  }
};
</script>

<style scoped>

.progress__container {
    width: 90%;
    background-color:#747D88;
    border-radius: 5px;
    line-height: 5px;
    height: 7px;
    margin:auto;
}

.progress__bar {
    height: 7px;
    background: linear-gradient(90deg, #F27A54 0%, #A154F2 100%);
    box-shadow: 0px 5px 10px rgba(207, 111, 138, 0.15);
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    display: inline-block;
}

.progress {
    position: relative;
    height:140px;
    background:transparent;
}

.step {
    position: absolute;
    transform: translate(-50%, 0);
    text-align: center;
    margin-top: -40px;
    height: 100px;
    width:100px;
}

.step__content {
    display: inline-block;
    margin-top: 11px;
}

.Endstep {
    position: absolute;
    transform: translate(-50%, 0);
    text-align: center;
    margin-top: -60px;
    height: 140px;
    width:100px;
}

.EndTitle {
    font-family: Montserrat;
    font-style: normal;
    font-weight: bold;
    font-size: 12px;
    line-height: 14px;
    text-align: center;
    color: #FFFFFF;
    margin-top: 0px;
    margin-bottom: 0px;
}

.EndIcon{
    position:absolute;
    transform: none;
    text-align: right;
    width: 4px;
    height: 20px;
    background: #FFFFFF;
    border-radius: 3px;
    margin-top:28px;
    z-index:10;
}

.EndValue {
    font-family: Montserrat;
    font-style: normal;
    font-weight: bold;
    font-size: 12px;
    line-height: 12px;
    text-align: center;
    color: #FFFFFF;
    margin-top:90px;
}

.currentProgressTitle{
    font-family: Montserrat;
    font-style: normal;
    font-weight: bold;
    font-size: 12px;
    line-height: 12px;
    text-align: center;
    color: #FFFFFF;
    margin-top: 0px;
    margin-bottom: 0px;
}

.CurrentProgressIcon{
    animation: BeginingPointPulse 3s linear infinite;
    font-size: 13px;
    font-weight: bold;
    border-radius: 14px;
    position: absolute;
    height: 4px;
    width: 4px;
    left: 50%;
    color: black;
    background-color: #FF5773;
    transform: translate(-50%, 0);
    padding: 5px;
    text-align: center;
    top:38px;
    z-index:100;
}

.currentProgressValue{
    font-family: Montserrat;
    font-style: normal;
    font-weight: bold;
    font-size: 12px;
    line-height: 12px;
    text-align: center;
    color: #FFFFFF;
    margin-top:50px;
}


@keyframes BeginingPointPulse{
    0%{
        box-shadow: 0 0 0 0 rgba(255,109,74,.7), 0 0 0 0 rgba(255,109,74,.7);
    }
    40%{
        box-shadow: 0 0 0 20px rgba(255,109,74 ,0), 0 0 0 0 rgba(255,109,74,.7);
    }
    80%{
        box-shadow: 0 0 0 20px rgba(255,109,74 , 0), 0 0 0 10px rgba(255,109,74,0);
    }
    100%{
        box-shadow: 0 0 0 0 rgba(255,109,74 ,0),0 0 0 10px rgba(255,109,74,0);
    }
}

</style>
