<template>
  <div v-if="messageString" id="alert_container" class="aat-alert">
    <b-alert variant="primary" show>
      Assignment submitted for {{ messageString }}.
      <div class="aat-note">
        This may take up to 10 minutes before the changes are visible everywhere.
      </div>
    </b-alert>
  </div>
</template>

<script>
  export default {
    name: "MessageArea",
    components: {
    },
    props: {
      messageString: {
        type: String,
        default: ""
      },
    },
    data() {
      return {
        id: ''
      };
    },
    methods: {
    }
  };
</script>

<style lang="scss">
  .aat-alert {
    margin: 1rem auto;
    max-width: 100%;
  }

  .aat-alert {
    a {
      color: inherit;
      text-decoration: underline;
    }

    .aat-note {
      font-size: 0.8125rem;
      padding-top: 0.25rem;
    }
  }
</style>
