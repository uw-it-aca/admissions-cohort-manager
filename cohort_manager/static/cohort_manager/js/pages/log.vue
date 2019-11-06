<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Activity Log
    </h1>
    <activitylist />
  </div>
</template>

<script>
  import ActivityList from "../components/activity_list.vue";
  export default {
    name: "Log",
    components: {
      activitylist : ActivityList
    },
    data(){
      return {};
    },
    mounted() {},
    beforeMount(){},
  };
</script>

<style lang="scss">
</style>
