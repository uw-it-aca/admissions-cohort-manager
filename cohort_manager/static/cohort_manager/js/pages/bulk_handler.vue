<template>
  <p>Bulk handler</p>
</template>

<script>

  // const axios = require("axios");
  export default {
    name: "BulkHandler",
    components: {
    },
    data(){
      return {
        upload_id: undefined
      };
    },
    params: {
    },
    computed: {
    },
    watch: {
      upload_id: function(){

      }
    },
    mounted() {
      this.upload_id = this.$route.params.id;
    },
    methods: {

    }
  };
</script>

<style lang="scss">
</style>
