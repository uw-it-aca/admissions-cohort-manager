<template>
  <div>
    <p>Bulk handler</p>
    <p v-if="err_msg">
      {{ err_msg }}
    </p>
    <pre v-if="upload_data">{{ upload_data }}</pre>
  </div>
</template>

<script>

  const axios = require("axios");
  export default {
    name: "BulkHandler",
    components: {
    },
    data(){
      return {
        upload_id: undefined,
        upload_data: undefined,
        err_msg: undefined
      };
    },
    params: {
    },
    computed: {
    },
    watch: {
      upload_id: function(){
        this.get_upload();
      }
    },
    mounted() {
      this.upload_id = this.$route.params.id;
    },
    methods: {
      get_upload(){
        var vue = this;
        axios.get(
          '/api/upload/' + this.upload_id + '/',
        ).then(response => {
          vue.upload_data = response.data;
        }).catch(function (err_resp) {
          vue.err_msg = err_resp.response.data.error;
        });
      }
    }
  };
</script>

<style lang="scss">
</style>
