<template>
  <div :class="env_class">
    Welcome To {{ env_string }}
  </div>
</template>

<script>
  export default {
    name: "EnvBanner",
    components: {
    },
    data() {
      return {
        env: '',

      };
    },
    computed: {
      env_string() {
        if(this.env === "localdev"){
          return "Local Dev";
        } else if(this.env === "eval") {
          return "AAT Test";
        } else if(this.env === "prod") {
          return "AAT Production";
        }
        return "Unknown";
      },
      env_class(){
        return "aat-env-" + this.env;
      }
    },
    mounted() {
      /*global aat_env*/
      this.env = aat_env;
    },
  };
</script>

<style lang="scss">
</style>
