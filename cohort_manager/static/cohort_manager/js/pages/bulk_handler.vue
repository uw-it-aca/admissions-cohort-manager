<template>
  <div>
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
        v-if="collection_options"
        :upload-response="upload_data"
        :collection-type="collection_type"
        upload-type="bulk"
        :collection-options="collection_options"
        :collection-id="collection_id"
        @is-reassign="handle_reassign"
        @is-reassign_protected="handle_reassign_protected"
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
        cohort_data: undefined,
        major_data: undefined,
        comment: '',
        is_reassign_protected: false,
        is_reassign: false,
        csrfToken: '',
        submit_msg: '',
        collection_options: undefined
      };
    },
    params: {
    },
    computed: {
      collection_type(){
        if(this.upload_data !== undefined){
          if(this.upload_data.cohort !== null){
            return "Cohort";
          } else if(this.upload_data.major !== null){
            return "Major";
          }
        }
        return undefined;
      },
      current_period(){
        if(this.upload_data !== undefined){
          return this.upload_data.quarter;
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
      collection_data() {
        if(this.collection_type == "Cohort"){
          return this.cohort_data;
        }
        if(this.collection_type == "Major"){
          return this.major_data;
        }
        return null;
      }
    },
    watch: {
      upload_id: function(){
        this.get_upload();
      },
      upload_data(){
        this.get_collection_options();
      }
    },
    mounted() {
      this.upload_id = this.$route.params.id;
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = window.csrf_token;
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
      set_collection_data(){
        var vue = this;
        $(this.collection_options).each(function(idx, val){
          if(val.value.toString() === vue.collection_id){
            if(vue.collection_type === "Cohort"){
              vue.cohort_data = {
                admit_decision : val.admit_decision,
                applications_assigned : val.assigned_count,
                description : val.description,
                protected_group : val.protected,
                residency : val.residency,
                collection_id : val.value
              };
            } else if (vue.collection_type === "Major"){
              vue.major_data = {
                collection_id : val.abbr,
                applications_assigned : val.assigned_count,
                display_name : val.text,
                college : val.college,
                division : val.division,
                program_code : val.value,
                dtx: val.dtx
              };
            }

          }
        });
      },
      get_collection_options(){
        var vue = this,
            url = undefined;
        if(this.collection_type === 'Cohort') {
          url ='/api/collection/cohort/' + this.current_period + "/";
        }
        if(this.collection_type === 'Major'){
          url = '/api/collection/major/' + this.current_period + "/";
        }
        if(url !== undefined){
          axios.get(
            url
          ).then(response => {
            vue.collection_options = response.data;
            vue.set_collection_data();
          });
        }
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
