<template>
  <div>
    <p>Bulk handler</p>
    <p v-if="fetch_err_msg">
      {{ fetch_err_msg }}
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
        upload-type="bulk"
        :collection-options="collection_options"
        :collection-id="collection_id"
        @is_reassign="handle_reassign"
        @is_reassign_protected="handle_reassign_protected"
      />
      <collection-comment
        @comment="update_comment"
      />
      <b-button type="submit" variant="primary" @click="submit_collection">
        Submit
      </b-button>
      <b-modal
        ref="submitting_modal"
        modal-class="aat-modal-box"
        content-class="aat-modal"
        hide-backdrop
        :hide-footer="true"
        :hide-header="true"
        :hide-header-close="true"
        :no-close-on-backdrop="true"
        :no-close-on-esc="true"
      >
        <div v-if="submit_msg">
          {{ submit_msg }}
        </div>
        <div v-else>
          <div class="text-center text-info aat-processing-text">
            <b-spinner class="align-middle" />
            <strong>Processing...</strong>
          </div>
          <p class="text-center aat-processing-message">
            Please wait while your submission is processed.
          </p>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>

  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  import UploadReview from "../components/collection_upload_review.vue";
  import CollectionComment from "../components/collection_comment.vue";
  export default {
    name: "BulkHandler",
    components: {
      CollectionDetails,
      UploadReview,
      CollectionComment
    },
    data(){
      return {
        upload_id: undefined,
        upload_data: undefined,
        fetch_err_msg: undefined,
        collection_data: undefined,
        comment: '',
        is_reassign_protected: false,
        is_reassign: false,
        csrfToken: '',
        submit_msg: ''
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
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      handle_reassign(is_reassign){
        this.is_reassign = is_reassign;
      },
      handle_reassign_protected(is_reassign_protected){
        this.is_reassign_protected = is_reassign_protected;
      },
      get_upload(){
        var vue = this;
        axios.get(
          '/api/upload/' + this.upload_id + '/',
        ).then(response => {
          vue.upload_data = response.data;
        }).catch(function (err_resp) {
          vue.fetch_err_msg = err_resp.response.data.error;
        });
      },
      get_collection_data(){
        var vue = this;
        axios.get(
          '/api/collection/' + this.collection_type.toLowerCase() + "/" + this.current_period + "/" + this.collection_id + "/",
        ).then(response => {
          vue.collection_data = response.data;
        }).catch(function () {});
      },
      update_comment(comment){
        this.comment = comment;
      },
      submit_collection(){
        var vue = this,
            request = {'is_submitted': true,
                       'is_reassign': this.is_reassign,
                       'is_reassign_protected': this.is_reassign_protected,
                       'comment': this.comment};
        this.$refs['submitting_modal'].show();
        if (this.collection_type == "Cohort") {
          request.cohort_id = this.collection_id;
        } else if (this.collection_type == "Major") {
          request.major_id = this.collection_id;
        }
        axios.put(
          '/api/upload/' + this.upload_id + "/",
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function(response) {

          console.log(JSON.stringify(response.data.request)); // eslint-disable-line
          vue.$refs['submitting_modal'].hide();
          if(response.status === 200) {
            vue.navigate_after_submit();
          }else if(response.status === 202){
            vue.$refs['submitting_timeout_modal'].show();
          }

        }).catch(function (error) {
          if (error.response) {
            vue.submit_msg = "Error making submission.";
          } if (error.response.status === 543){
            vue.submit_msg += " There was an issue with the AdSel API.";
          }
        });
      },
      navigate_after_submit() {
        this.$router.push({path: '/iframe/log/'});
      },
    }
  };
</script>

<style lang="scss">
</style>
