<template>
  <div class="aat-iframe-base">
    <main ref="main" aria-labelledby="aat_page_header" class="col aat-main-container">
      <router-view />
    </main>
  </div>
</template>

<script>

  export default {
    name: "IFrameBase",
    components: {
    },
    data(){
      return {
      };
    },
    computed: {
    },
    watch: {
    },
    mounted() {
    },
    methods: {

    }
  };
</script>

<style lang="scss">
  .aat-globalenv-eval,
  .aat-globalenv-prod {
    background-color: #fff;
  }

  .aat-iframe-base {
    // Display of cohort and major details in iframe
    background-color: #fff;

    .aat-form-section.aat-details-container {
      padding: 0.5rem 1rem !important;
    }

    .aat-group-info-primary,
    .aat-group-info-secondary {
      margin-bottom: 0.5rem !important;
    }

    .aat-info-spacing {
      padding-bottom: 0 !important;
    }

    .aat-data-primary .aat-group-data {
      font-size: 1.5rem !important;
    }

    // Add Comment section in iframe

    .aat-comment-field {
      height: 4rem;
    }
  }
</style>
