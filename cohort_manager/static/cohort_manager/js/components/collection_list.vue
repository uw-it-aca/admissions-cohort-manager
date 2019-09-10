<template>
  <div>
    <h2>Collection List {{ collectionType }}</h2>
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
