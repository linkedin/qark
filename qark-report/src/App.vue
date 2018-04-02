<template>
  <router-view></router-view>
</template>

<script>
  import Card from 'bootstrap-vue/src/components/card/card'
  export default {
    name: 'app',
    components: {
      Card
    }
  }
</script>

<style>
  /* Import Font Awesome Icons Set */
  $fa-font-path: '~font-awesome/fonts/';
  @import '~font-awesome/css/font-awesome.min.css';
  /* Import Simple Line Icons Set */
  $simple-line-font-path: '~simple-line-icons/fonts/';
  @import '~simple-line-icons/css/simple-line-icons.css';
  /* Import Bootstrap Vue Styles */
  @import '~bootstrap-vue/dist/bootstrap-vue.css';
</style>
<style lang="scss">
  // Import Main styles for this application
  @import './scss/style';
  .vulnerability{
    color: white;
    vertical-align: center;
    height: 20px;
    /*width: 120px;*/
    font-family: Helvetica;
    line-height: 20px;
    font-weight: bold;
    background-color: #f75d5c
  }
  .warning{
    color: white;
    vertical-align: center;
    height: 20px;
    font-family: Helvetica;
    line-height: 20px;
    font-weight: bold;
    background-color: #ffc107
  }
  .info{
    color: white;
    vertical-align: center;
    height: 20px;
    font-family: Helvetica;
    line-height: 20px;
    font-weight: bold;
    background-color: #2eadd3
  }
  .debug{
    color: white;
    vertical-align: center;
    height: 20px;
    font-family: Helvetica;
    line-height: 20px;
    font-weight: bold;
    background-color: #0161a1;
  }
</style>
