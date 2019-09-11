<template>
  <div>
    <h2>Collection List {{ collectionType }}</h2>
    <div v-if="collectionType === 'Cohort'">You, Cohort, you!</div>
    <div v-else-if="collectionType === 'Major'">You, Major, you!</div>
    <div v-else>Error: There was an issue with your request. Please select a link from the left column to try again.</div>
  </div>
</template>

<script>
  export default {
    name: "CollectionList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        
      };
    },
    mounted() {

    },
    methods: {
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

</style>
