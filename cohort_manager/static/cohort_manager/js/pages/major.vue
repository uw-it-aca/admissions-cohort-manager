<template>
  <div>
    <h1>Assign Major</h1>
    <p>this is the major page stub</p>
    <p>Showing data for {{ cohort_code }} cohort</p>
  </div>
</template>

<script>
  export default {
    name: "Major",
    components: {},
    data(){
      return {
        cohort_code: ""
      };
    },
    mounted() {},
    beforeMount(){
      this.cohort_code = $("#cohort").attr('data');
    },
  };
</script>

<style lang="scss">
</style>
