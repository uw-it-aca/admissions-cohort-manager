<template>
  <div>
    <h1 class="aat-page-header">
      All Majors
    </h1>
    <collectionlist collection-type="Major"/>
    <div>
    </div>
  </div>
</template>

<script>
  import CollectionList from "../components/collection_list.vue";
  export default {
    name: "MajorList",
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
