<template>
  <div>
    <p>Bulk handler</p>
    <p v-if="err_msg">
      {{ err_msg }}
    </p>
    <div v-if="upload_data">
      <collection-details
        :collection-type="collection_type"
        :collection-id="collection_id"
        :current-period="current_period"
      />
    </div>
  </div>
</template>

<script>

  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  export default {
    name: "BulkHandler",
    components: {
      CollectionDetails
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
      collection_type(){
        if(this.upload_data !== undefined){
          if(this.upload_data.cohort !== null){
            return "cohort";
          } else if(this.upload_data.major !== null){
            return "major";
          }
        }
        return undefined;
      },
      current_period(){
        if(this.upload_data !== undefined){
          return this.upload_data.quarter.toString();
        }
        return undefined;
      },
      collection_id() {
        if (this.upload_data !== undefined) {
          if (this.upload_data.cohort !== null) {
            return this.upload_data.cohort;
          } else if (this.upload_data.major !== null) {
            return this.upload_data.major;
          }
        }
        return undefined;
      }
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
