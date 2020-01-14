<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      All Cohorts
    </h1>
    <collectionlist
      collection-type="Cohort"
      :admissions_period="admissions_period"
      v-on="$listeners"
    />
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
        admissions_period: this.$attrs.cur_period

      };
    },
    mounted() {},
    methods: {

    },
  };
</script>

<style lang="scss">
</style>
