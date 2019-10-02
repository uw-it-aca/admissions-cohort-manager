<template>
  <div>
    <h1 class="aat-page-header">
      Assign Cohort
    </h1>
    <component :is="currentComponent" v-bind="currentProperties" @uploaded="onFileUpload" />
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  import UploadReview from "../components/collection_upload_review.vue";

  export default {
    name: "Cohort",
    components: {
      upload: Upload,
      uploadReview: UploadReview,
    },
    data(){
      return {
        has_uploaded: false,
        upload_response: undefined,
        cohort_options: [
          {value: '1', text: '1'},
          {value: '2', text: '2'},
          {value: '99', text: '99'},
        ]
      };
    },
    computed: {
      currentComponent: function () {
        if(this.has_uploaded){
          return "uploadReview";
        } else {
          return "upload";
        }

      },
      currentProperties: function() {
        var properties = {collectionType: 'Cohort'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.cohort_options;
        properties['uploadResponse'] = this.upload_response;
        return properties;
      }
    },
    mounted() {
    },
    methods: {
      onFileUpload(response){
        this.has_uploaded = true;
        this.upload_response = response.data;
      }
    }
  };
</script>

<style lang="scss">
</style>
