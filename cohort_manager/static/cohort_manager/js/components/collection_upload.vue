<template>
  <div>
    <form @submit.prevent="handleUpload">
      <div class="aat-form-section">
        <fieldset>
          <legend class="aat-sub-header">
            Select {{ collectionType }}
          </legend>
          <label for="collection_chooser">Assign applications to {{ collectionType }} </label>
          <b-form-select id="collection_chooser" v-model="collection_id" name="collection" :options="collectionOptions" class="aat-select-inline" />
        </fieldset>
        <collectionDetails
          :collection-id="collection_id"
          :collection-type="collectionType"
        />
      </div>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Enter Applications
        </legend>
        <div id="add_applications_widget">
          <component 
            :is="uploadComponent" 
            @fileselected="selectedFile" 
            @listupdated="selectedList"
          />
          <div>
            or 
            <b-button id="manual_toggle" v-b-modal.add_list_modal variant="link">
              {{ uploadToggleLabel }}
            </b-button>
            <b-modal id="add_list_modal" title="Add Applicantions" ok-title="Done">
              <CollectionUploadListInput />
            </b-modal>
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
      <input type="submit" value="Upload">
    </form>
  </div>
</template>

<script>
  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  import CollectionUploadListInput from "../components/collection_upload_list_input.vue";
  import CollectionUploadFileInput from "../components/collection_upload_file_input.vue";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Upload",
    components: {
      collectionDetails: CollectionDetails,
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
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
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
        }).catch(function () {
          this.uploadResponse = "THERE WAS AN ERROR";
        });
      },

      toggleUpload() {
        this.manual_upload = !this.manual_upload;
        return false;
      },
      selectedFile(file) {
        this.file = file;
      },
      selectedList(list) {
        this.syskey_list = list;
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

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

  .aat-checkbox {
    margin-top: 2rem;
  }

  .aat-status-feedback {
    font-style: italic;
    margin-top: 1.5rem;
  }

</style>
