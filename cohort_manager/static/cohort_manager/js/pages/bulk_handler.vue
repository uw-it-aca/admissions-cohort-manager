<template>
  <div>
    <p>Bulk handler</p>
    <p v-if="err_msg">
      {{ err_msg }}
    </p>
    <div v-if="upload_data">
      <collection-details
        :collection-type="collection_type"
        :current-period="current_period"
        :collection-data="collection_data"
      />
      <upload-review
        :upload-response="upload_data"
        :collection-type="collection_type"
        upload-type="file"
        :collection-options="collection_options"
        :collection-id="collection_id"
      />
      <!--                     @upload_reset="handleReset"-->
      <!--                     @is_reassign="handle_reassign"-->
      <!--                     @is_reassign_protected="handle_reassign_protected"-->
    </div>
  </div>
</template>

<script>

  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  import UploadReview from "../components/collection_upload_review.vue";
  export default {
    name: "BulkHandler",
    components: {
      CollectionDetails,
      UploadReview
    },
    data(){
      return {
        upload_id: undefined,
        upload_data: undefined,
        err_msg: undefined,
        collection_data: undefined
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
      },
      collection_options(){
        if (this.upload_data !== undefined) {
          return [{'text': 'foo','description': 'bar', 'protected': false}];
        }
        return undefined;
      }
    },
    watch: {
      upload_id: function(){
        this.get_upload();
      },
      collection_id() {
        if(this.collection_id !== undefined && this.current_period !== undefined && this.collection_type !== undefined){
          this.get_collection_data();
        }

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
      },
      get_collection_data(){
        var vue = this;
        axios.get(
          '/api/collection/' + this.collection_type.toLowerCase() + "/" + this.current_period + "/" + this.collection_id + "/",
        ).then(response => {
          vue.collection_data = response.data;
        }).catch(function () {});
      }
    }
  };
</script>

<style lang="scss">
</style>
