<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      All Cohorts
    </h1>
    <collectionlist collection-type="Cohort" />
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
