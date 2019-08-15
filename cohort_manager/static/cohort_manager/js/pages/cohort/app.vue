<template>
    <div>
    <p>this is the cohort page stub</p>
    <p>Showing data for {{ cohort_code }} cohort</p>
    </div>
</template>

<script>
  export default {
    name: "Cohort",
    components: {},
    mounted() {},
    data(){
      return {
        cohort_code: ""
      }
    },
    beforeMount(){
      this.cohort_code = $("#cohort").attr('data');
    },
  };
</script>

<style lang="scss">
</style>
