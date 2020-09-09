<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: green;
  margin-top: 60px;
}
// https://color.adobe.com/zh/create/color-wheel
// 選定主色後
// 字色從複合找
// hover, focus, active從濃度找 

.custom1 {
  background-color: #a6c2ce;
  border-color: #a6c2ce;
  color: #2B3669;
  &:hover{
    background-color: #93ABB5;
    border-color: #93ABB5;
    color: #2B3669;
  }
  &:focus{
    color: #2B3669;
    background-color: #93ABB5;
    border-color: #93ABB5;
    box-shadow: 0 0 0 0.2rem #B2CFDB !important;
  }
  &:active{
    color: #2B3669 !important;  
    background-color: #93ABB5 !important;
    border-color: #93ABB5 !important;
  }

}
.custom2 {
  background-color: #9c8f96;
}
.custom3 {
  background-color: #ebc57c;
}
.custom4 {
  background-color: #6b799e;
}
</style>
