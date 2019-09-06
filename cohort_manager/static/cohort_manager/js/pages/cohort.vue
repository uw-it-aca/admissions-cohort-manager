<template>
  <div>
    <h1>Assign Cohort</h1>
    <p>this is the chort page stub</p>
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
