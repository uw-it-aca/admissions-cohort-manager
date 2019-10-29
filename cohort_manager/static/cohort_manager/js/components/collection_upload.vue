<template>
  <div>
    <form @submit.prevent="">
      <div class="aat-form-section">
        <fieldset class="aat-collection-select">
          <legend class="aat-sub-header">
            Select {{ collectionType }}
          </legend>
          <label for="collection_chooser">Assign applications to {{ collectionType }} </label>
          <b-form-input id="input-with-list" v-model="collection_id" list="input-list" class="aat-select-inline" required/>
          <b-form-datalist id="input-list" :options="collectionOptions" />
        </fieldset>
        <collectionDetails
          v-if="collectionType === 'Cohort'"
          :collection-id="collection_id"
          :collection-type="collectionType"
        />
      </div>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Enter Applications
        </legend>
        <div id="add_applications_widget">
          <upload-review v-if="has_uploaded"
                         :upload-response="upload_response"
                         :collection-type="collection_type"
                         @upload_reset="handleReset"
                         @dupeToRemove="handleRemove"
          />
          <div v-else>
            <div>
              Enter applications by file (csv) or
              <b-button id="manual_toggle" v-b-modal.add_list_modal class="aat-btn-link" variant="link">
                {{ uploadToggleLabel }}
              </b-button>
              <CollectionUploadListInput @listupdated="selectedList" />
            </div>
            <component
              :is="uploadComponent"
              @fileselected="selectedFile"
            />
          </div>
        </div>
      </fieldset>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Add Comment
        </legend>
        <label for="assignment_comment">Enter comment for this assignment</label>
        <textarea id="assignment_comment" v-model="comment" class="aat-comment-field" />
      </fieldset>
      <b-button type="submit" variant="primary" @click="mark_for_submission">
        Submit
      </b-button>
    </form>
  </div>
</template>

<script>
  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  import CollectionUploadListInput from "../components/collection_upload_list_input.vue";
  import CollectionUploadFileInput from "../components/collection_upload_file_input.vue";
  import UploadReview from "../components/collection_upload_review.vue";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Upload",
    components: {
      collectionDetails: CollectionDetails,
      uploadReview: UploadReview,
      CollectionUploadListInput: CollectionUploadListInput,
      CollectionUploadFileInput: CollectionUploadFileInput
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
      collectionOptions: {
        type: Array,
        default: function () {return[];}
      }
    },
    data(){
      return {
        file: null,
        syskey_list: null,
        collection_id: null,
        comment: '',
        csrfToken: '',
        manual_upload: false,
        upload_toggle_label_file: "by file",
        upload_toggle_label_manual: "manually by system keys",
        has_uploaded: false,
        upload_response: undefined,
        collection_type: this.$props.collectionType,
        to_remove: []
      };
    },
    computed: {
      uploadComponent: function () {
        if (this.manual_upload) {
          return "CollectionUploadListInput";
        } else {
          return "CollectionUploadFileInput";
        }
      },
      uploadToggleLabel: function() {
        if (!this.manual_upload) {
          return this.upload_toggle_label_manual;
        } else {
          return this.upload_toggle_label_file;
        }
      }
    },
    mounted() {
      if (this.$route.params.id !== undefined) {
        this.selectCollection(this.$route.params.id);
      }
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      handleReset() {
        this.has_uploaded = false;
        this.upload_response = undefined;
      },
      handleRemove(to_remove) {
        this.to_remove = to_remove;
      },
      handleUpload() {
        let formData = new FormData();
        if (this.file !== null){
          formData.append('file', this.file);
        } else  if (this.syskey_list !== null){
          formData.append('syskey_list', this.syskey_list);
        }
        formData.append('comment', this.comment);
        if (this.collectionType == "Cohort") {
          formData.append('cohort_id', this.collection_id);
        } else if (this.collectionType == "Major") {
          formData.append('major_id', this.collection_id);
        } else {
          this.uploadResponse = "THERE WAS AN ERROR";
          return;
        }
        axios.post(
          '/api/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(response => {
          this.$emit('uploaded', response);
          this.has_uploaded = true;
          this.upload_response = response.data;
        }).catch(function () {
          this.uploadResponse = "THERE WAS AN ERROR";
        });
      },

      mark_for_submission(){

        var vue = this,
            request = {'submit': true,
                       'is_reassign': this.is_reassign,
                       'is_reassign_protected': this.is_reassign_protected,
                       'to_delete': this.to_remove};
        axios.put(
          '/api/upload/' + this.upload_response.id + "/",
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function() {
          vue.$emit('showMessage', vue.upload_response.id.toString());
          if(vue.collection_type == "Cohort"){
            vue.$router.push({path: '/cohort_list'});
          } else if(vue.collection_type == "Major"){
            vue.$router.push({path: '/major_list'});
          }


        });
      },

      toggleUpload() {
        this.manual_upload = !this.manual_upload;
        return false;
      },
      selectedFile(file) {
        this.file = file;
        this.handleUpload();
      },
      selectedList(list) {
        this.syskey_list = list;
        this.handleUpload();
      },
      selectCollection(id){
        // Only allow options that are in list
        var id_to_set;
        $(this.collectionOptions).each(function(idx, option){
          if (id === option.value){
            id_to_set = id;
          }
        });
        if (id_to_set !== undefined){
          this.collection_id = id_to_set;
        }

      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  // form fields
  .aat-file-input {
    padding: 1rem 0;
  }

  .aat-comment-field {
    display: block;
    height: 144px;
    max-width: 650px;
    min-width: 250px;
    padding: 0.5rem;
    width: 100%;
  }

  .aat-collection-select {
    .aat-collection-select-label {
      display: inline-block;
      margin-right: 0.5rem;
    }

    .aat-select-inline {
      display: inline-block;
      margin-left: 0.25rem;
    }
  }

  // form messaging
  .aat-status-feedback {
    font-size: 0.75rem;
  }

  // action elements
  .aat-btn-link {
    padding: 0 !important;
    vertical-align: baseline !important;
  }

</style>
