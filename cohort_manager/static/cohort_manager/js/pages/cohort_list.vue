<template>
  <div>
    <h1 class="aat-page-header">
      All Cohorts
    </h1>
    <collectionlist collection-type="Cohort"/>
    <div>
    </div>
  </div>
</template>

<script>
  import CollectionList from "../components/collection_list.vue";
  export default {
    name: "CohortList",
    components: {
      collectionlist : CollectionList
    },
    data(){
      return {
        
      };
    },
    mounted() {},
    methods: {
      
    }
  };
</script>

<style lang="scss">
</style>
