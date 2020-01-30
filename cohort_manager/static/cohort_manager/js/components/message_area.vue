<template>
  <div v-if="messageString" id="alert_container" class="aat-alert">
    <b-alert v-if="alert_type === 'primary'" variant="primary" show>
      {{ messageString }}
    </b-alert>
    <b-alert v-if="alert_type === 'success'" variant="success" show>
      {{ messageString }}
    </b-alert>
    <b-alert v-if="alert_type === 'error'" variant="danger" show>
      {{ messageString }}
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
      alertType: {
        type: String,
        default: "primary"
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
