<template>
  <div>
    <h2>Collection List {{ collectionType }}</h2>
    <p v-if="collectionType === 'Cohort'">You, Cohort, you!</p>
    <p v-else-if="collectionType === 'Major'">You, Major, you!</p>
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
