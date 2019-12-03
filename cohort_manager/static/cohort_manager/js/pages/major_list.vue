<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      All Majors
    </h1>
    <collectionlist
      collection-type="Major"
      :admissions_period="admissions_period"
    />
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
        admissions_period: this.$attrs.cur_period
      };
    },
    mounted() {},
    methods: {

    }
  };
</script>

<style lang="scss">
</style>
