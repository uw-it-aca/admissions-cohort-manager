<template>
  <div>
    <div v-if="collectionType === 'Cohort'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="is_loading"
        :items="cohorts"
        :fields="cohortFields"
      >
        <template v-slot:cell(actions)="row">
          <a :href="'/cohort/' + row.item.value" :title="'Assign applications to cohort ' + row.item.value">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to cohort ' + row.item.value" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
        <template v-slot:table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>

    <div v-else-if="collectionType === 'Major'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="is_loading"
        :items="majors"
        :fields="majorFields"
      >
        <template v-slot:cell(actions)="row">
          <a :href="'/major/' + row.item.value" :title="'Assign applications to major ' + row.item.value">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to major' + row.item.value" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
        </template>
        <template v-slot:table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>

    <div v-else>
      Error: There was an issue with your request. Please select a link from the left column to try again.
    </div>

    <!-- Reset Collection modal -->
    <template>
      <div>
        <b-modal
          :id="resetModal.id"
          modal-class="aat-modal-box"
          content-class="aat-modal"
          hide-backdrop
          :title="resetModal.title"
          ok-only
          :ok-title="'Reset ' + collectionType"
          :ok-disabled="resetModal.ok_disabled"
          @hide="resetResetModal"
          @ok="submit_reset"
        >
          <form @submit.prevent="handleUpload">
            <div>
              <fieldset class="aat-form-section">
                <legend class="aat-sub-header">
                  Confirm Reset
                </legend>
                <div id="reset_col_option">
                  <b-form-checkbox
                    id="col_reset_checkbox"
                    v-model="checked"
                    name="col_reset_checkbox"
                    value=""
                  >
                    Reassign all applications from "<span v-if="collectionType === 'Cohort'">Cohort </span>{{ resetModal.itemId }}" to <em>unassigned</em>.
                  </b-form-checkbox>
                </div>
              </fieldset>
              <fieldset class="aat-form-section">
                <legend class="aat-sub-header">
                  Add Comment
                </legend>
                <label for="reassignment_comment">Enter comment for this assignment.</label>
                <textarea id="reassignment_comment" v-model="comment" class="aat-comment-field" />
              </fieldset>
              <p v-if="resetModal.protect === 'Yes'">
                <b>Note:</b> This is a protected cohort.
              </p>
            </div>
          </form>
        </b-modal>
      </div>
    </template>
  </div>
</template>

<script>
  const axios = require("axios");
  import { EventBus } from "../main";
  export default {
    name: "CollectionList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        cohortFields: [
          {
            key: 'value',
            label: "Cohort #",
            class: "aat-data-cell aat-data-nowrap center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'description',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'residency',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'protected',
            label: 'Protected',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'admit_decision',
            class: "aat-data-cell aat-data-nowrap center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_count',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          { key: 'actions',
            label: '',
            class: "aat-actions-cell aat-data-cell aat-data-nowrap", },
        ],
        cohorts: [],
        majorFields: [
          {
            key: 'value',
            label: 'Major Code',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'text',
            label: 'Major',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'division',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'college',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'dtx',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_count',
            class: "aat-data-cell center",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'Actions',
            label: '',
            class: "aat-actions-cell aat-data-cell aat-data-nowrap",
            sortable: false,
          }
        ],
        majors: [],
        resetModal: {
          id: 'reset-modal',
          title: '',
          itemId: '',
          ok_disabled: true
        },
        checked: false,
        comment: '',
        admissions_period: null,
        is_loading: true
      };
    },
    watch: {
      checked: function(val){
        if(val === false){
          this.resetModal.ok_disabled = true;
        } else {
          this.resetModal.ok_disabled = false;
        }
      }
    },
    mounted() {
      this.setCSRF();
    },
    created(){
      this.admissions_period = this.$attrs.admissions_period;
      this.load_data();
      EventBus.$on('period_change', period => {
        this.admissions_period = period;
        this.load_data();
      });
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      load_data(){
        this.is_loading = true;
        axios.get(
          '/api/collection/'
            + this.collectionType.toLowerCase()
            + "/"
            + this.admissions_period
            + "/",
        ).then(response => {
          if(this.collectionType.toLowerCase() === "cohort"){
            this.cohorts = response.data;
          } else if (this.collectionType.toLowerCase() === "major"){
            this.majors = response.data;
          }
          this.is_loading = false;
        });
      },
      info(item, index, button) {
        this.resetModal.title = `Reset ${this.collectionType}`;
        this.resetModal.itemId = `${item.value}`;
        this.resetModal.protect = `${item.protect}`;
        this.$root.$emit('bv::show::modal', this.resetModal.id, button);
      },
      resetResetModal() {
        this.resetModal.title = '';
        this.resetModal.content = '';
        this.checked = false;
        this.resetModal.ok_disabled = true;
        this.load_data();
      },
      submit_reset(){
        var vue = this;
        // disable submit after click
        this.resetModal.ok_disabled = true;
        axios.delete(
          '/api/collection/'
            + this.collectionType.toLowerCase()
            + "/"
            + this.admissions_period
            + "/"
            + this.resetModal.itemId
            + "/",
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            },
            data: {comment: this.comment}
          },
        ).then(function() {
          vue.$emit('showMessage', vue.collectionType + " " + vue.resetModal.itemId + " has been reset.", "success");
        }).catch(function () {
          vue.$emit('showMessage', "Resetting " + vue.collectionType + " " + vue.resetModal.itemId + "was unsuccessful.", "error");
        });

      }
    }
  };
</script>

<style lang="scss">

  @import '../../css/_variables.scss';

  // Table action buttons
  .aat-actions-cell a,
  .aat-actions-cell button {
    color: $link-blue;
    font-family: 'Encode Sans Compressed',sans-serif;
    font-weight: bold;
    margin: 0 0.25rem;
    text-transform: uppercase;
  }

  .aat-actions-cell a i {
    color: $text-color;

    &:hover,
    &:focus {
      color: $link-blue;
    }
  }

  .aat-actions-cell.aat-data-cell .btn-secondary {
    background: none;
    border-style: none;
    color: $sub-header;
    font-size: 0.875rem;
    min-width: auto;
    padding: 0;
    vertical-align: baseline;

    &:hover,
    &:focus {
      color: $link-blue !important;
      text-decoration: underline;
    }
  }

</style>
