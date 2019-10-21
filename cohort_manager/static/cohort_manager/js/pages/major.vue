<template>
  <div>
    <h1 class="aat-page-header">
      Assign to Major
    </h1>
    <component :is="currentComponent" v-bind="currentProperties" @uploaded="onFileUpload" />
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  import UploadReview from "../components/collection_upload_review.vue";

  export default {
    name: "Major",
    components: {
      upload: Upload,
      uploadReview: UploadReview,
    },
    data(){
      return {
        has_uploaded: false,
        upload_response: undefined,
        major_options: [
          {value: 'CSE', text: 'Computer Science and Enginerding'},
          {value: 'CHEM', text: 'Chemistry'},
          {value: 'ART H', text: 'Art History'},
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
        var properties = {collectionType: 'Major'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.major_options;
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

