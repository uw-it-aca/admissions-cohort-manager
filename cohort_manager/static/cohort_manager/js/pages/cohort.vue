<template>
  <div>
    <h1 class="aat-page-header">Assign Cohort</h1>
    <upload @uploaded="onFileUpload" />
    <div>
      {{ upload_response }}
    </div>
  </div>
</template>

<script>
  import Upload from "../components/cohort_upload.vue";

  export default {
    name: "Cohort",
    components: {
      upload: Upload
    },
    data(){
      return {
        upload_response: undefined,
      };
    },
    mounted() {
    },
    methods: {
      onFileUpload(response){
        this.upload_response = response;
      }
    }
  };
</script>

<style lang="scss">
</style>
