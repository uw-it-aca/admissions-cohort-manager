<template>
  <div>
    <h1 class="aat-page-header">
      Assignment History
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
