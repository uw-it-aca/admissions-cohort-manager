<template>
  <div>
  <p>this is the cohort page stub</p>
  <p>Showing data for {{cohort_code}} cohort</p>
  </div>
</template>

<script>
  export default {
    name: "Cohort",
    components: {},
    mounted() {},
    beforeMount(){
        this.cohort_code = $("#cohort").attr('data');
    },
    data(){
        return {
            cohort_code: ""
        }
    }
  };
</script>

<style lang="scss">
</style>
