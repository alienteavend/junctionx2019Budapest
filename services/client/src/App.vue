<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  margin-top: 60px
}
html{
  background-color:#2e343b;
  color:#fff;
  margin: 0 15px;
}
body{
  background-color:#2e343b;
  color:#fff;
}
.card {
  background-color:#3a424a;
  border: none;
}

h1 {
  text-transform: uppercase;
  font-weight: bolder;
  background: -webkit-linear-gradient(left, #F07A56, #A255EB);
  background: -moz-linear-gradient(left, #F07A56, #A255EB);
  background: linear-gradient(to right, #F07A56, #A255EB);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.2em;
}

.card-title {
  color:#efefef;
}

.btn-pirates{
  border-radius:20px;
  background: -webkit-linear-gradient(left, #F07A56, #A255EB);
  background: -moz-linear-gradient(left, #F07A56, #A255EB);
  background: linear-gradient(to right, #F07A56, #A255EB);
  color: #fff;
  text-transform:uppercase;
  font-size: 14px;
  text-align:center;
  padding: 10px 20px;
  min-width: 220px;
  margin: 15px 0 5px 0;
}

.btn-pirates-disabled{
  background: -webkit-linear-gradient(left, rgb(241, 174, 154), rgb(202, 168, 235));
  background: -moz-linear-gradient(left,rgb(241, 174, 154), rgb(202, 168, 235));
  background: linear-gradient(to right,rgb(241, 174, 154), rgb(202, 168, 235));
}
</style>
