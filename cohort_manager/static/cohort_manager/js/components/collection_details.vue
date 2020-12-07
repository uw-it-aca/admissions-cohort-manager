<template>
  <b-container class="aat-details-container aat-form-section" fluid :hidden="hide_details">
    <div v-if="invalid_collection">
      <p>No {{ collectionType.toLowerCase() }} information available for <strong>{{ collectionType.toLowerCase() }} {{ collection_id }}</strong> in <strong>{{ currentPeriodName }}</strong> admission period.</p>
    </div>
    <div v-else>
      <b-row>
        <b-col class="aat-group-info-primary">
          <b-row class="aat-info-spacing">
            <b-col cols="3" class="aat-data-primary">
              {{ collectionType }}
              <div class="aat-group-data aat-data-primary">
                #{{ collection_id }}
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
      },
      currentPeriod: {
        type: Number,
        default: null
      },
      collectionData: {
        type: Object,
        default() {
          return {};
        }
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
        hide_details: true,
        periods: [],
        collection_id: "",
        collection_data: {}
      };
    },
    computed: {
      currentPeriodName: function () {
        var vue = this,
            value = "";
        $.each(vue.periods, function(idx, period){
          if(period['value'] === parseInt(vue.currentPeriod)){
            value = period['text'];
          }
        });
        return value;
      }
    },
    watch: {
      collectionId: function() {
        this.collection_id = this.collectionId;
        this.get_collection();
      },
      collectionData: {
        handler: function(){
          this.collection_data = this.collectionData;
          this.process_collection_data();
        },
        deep: true
      },
      collection_data: {
        handler: function(){
          this.process_collection_data();
        },
        deep: true
      }
    },
    created () {
      this.periods = this.$attrs.periods;
      if(Object.keys(this.collection_data).length === 0){
        if(this.collectionId !== null && this.collectionId.length > 0
          && this.collectionType.length > 0
          && this.cur_period !== null){
          this.get_collection();
        }
      } else {
        this.process_collection_data();
      }
    },

    methods: {
      get_collection(){
        var vue = this;
        this.hide_details = true;
        axios.get(
          '/api/collection/' + this.collectionType.toLowerCase() + "/" + this.currentPeriod + "/" + this.collectionId + "/",
        ).then(response => {
          this.collection_data = response.data;
        }).catch(function () {
          vue.invalid_collection = true;
          vue.hide_details = false;
        });
      },
      process_collection_data(){
        this.admit_decision = this.collection_data.admit_decision;
        this.applications_assigned = this.collection_data.applications_assigned;
        this.description = this.collection_data.description;
        this.protected_group = this.collection_data.protected_group;
        this.residency = this.collection_data.residency;
        this.invalid_collection = false;
        this.hide_details = false;
        this.collection_id = this.collection_data.collection_id;
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
      margin: 0.5rem 0 1.5rem;
      max-width: 650px;
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
    }

    .aat-group-info-secondary {
      margin-bottom: 1rem;
    }

  }

</style>
