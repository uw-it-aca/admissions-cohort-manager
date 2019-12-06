<template>
  <b-container v-if="collectionId" class="aat-details-container aat-form-section" fluid>
    <div v-if="invalid_collection">
      <p>You selected an invalid collection</p>
    </div>
    <div v-else>
      <b-row>
        <b-col class="aat-group-info-primary">
          <b-row class="aat-info-spacing">
            <b-col cols="3" class="aat-data-primary">
              {{ collectionType }}
              <div class="aat-group-data aat-data-primary">
                #{{ collectionId }}
              </div>
            </b-col>
            <b-col cols="9" class="aat-group-info-secondary">
              Description
              <div class="aat-group-data aat-data-baseline">
                {{ description }}
              </div>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row class="aat-group-info-secondary">
        <b-col class="aat-info-spacing">
          Residency <div class="aat-group-data">
            {{ residency }}
          </div>
        </b-col>
        <b-col class="aat-info-spacing">
          Protected <div class="aat-group-data">
            {{ protected_group }}
          </div>
        </b-col>
        <b-col class="aat-info-spacing">
          Admit Status<div class="aat-group-data">
            {{ admit_decision }}
          </div>
        </b-col>
        <b-col class="aat-info-spacing">
          Assigned
          <div class="aat-group-data">
            {{ applications_assigned }}
          </div>
        </b-col>
      </b-row>
    </div>
  </b-container>
</template>

<script>
  const axios = require("axios");
  import { EventBus } from "../main";

  export default {
    name: "CollectionDetails",
    components: {},
    props: {
      collectionType: {
        type: String,
        default: ""
      },
      collectionId: {
        type: String,
        default: ""
      }
    },
    data(){
      return {
        admit_decision: "",
        applications_assigned: 0,
        description: "",
        protected_group: false,
        residency: "",
        invalid_collection: false,
        current_period: undefined
      };
    },
    watch: {
      collectionId: function() {
        this.get_collection();
      }
    },
    created(){
      EventBus.$on('period_change', period => {
        this.current_period = period;
      });
    },
    mounted() {
    },
    methods: {
      get_collection(){
        var vue = this;
        axios.get(
          '/api/collection/' + this.collectionType.toLowerCase() + "/" + this.current_period + "/" + this.collectionId + "/",
        ).then(response => {
          this.admit_decision = response.data.admit_decision;
          this.applications_assigned = response.data.applications_assigned;
          this.description = response.data.description;
          this.protected_group = response.data.protected_group;
          this.residency = response.data.residency;
          this.invalid_collection = false;
        }).catch(function () {
          vue.invalid_collection = true;
        });
      }
    },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  // general layout
  .aat-form-section {
    &.aat-details-container {
      border: solid $banner-border 1px;
      color: $sub-header;
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 1.5rem 0 0;
      max-width: 800px;
      padding: 2rem;
    }
  }

  // labels and data

  .aat-group-info-primary {
    .aat-group-data {
      font-size: 2rem;

    }
  }

  .aat-group-data {
    color: $text-color;
    font-weight: bold;
  }

  .aat-info-spacing {
    padding-bottom: 1.5rem;
  }

  .aat-group-info-secondary {
    .row {
      align-items: unset;
      flex-direction: column;
      font-weight: normal;
      margin: 0 auto;
      padding: 0 25%;
    }

    .aat-group-data {
      font-size: 1rem;
      font-weight: normal;
    }

    .aat-info-spacing {
      padding-bottom: 1rem;
    }
  }

  // small screen overrides
  @media screen and (max-width: 767px) {
    .aat-group-info-primary {
      margin-bottom: 2rem;
      text-align: center;
    }

    .aat-group-info-secondary {
      margin-bottom: 1rem;
      text-align: center;
    }

  }

</style>
