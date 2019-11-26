<template>
  <div>
    <div v-if="collectionType === 'Cohort'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :items="cohorts"
        :fields="cohortFields"
      >
        <template v-slot:cell(actions)="row">
          <a :href="'/log/' + row.item.id" :title="'Activity for cohort ' + row.item.name"><i class="far fa-clock" /><span class="sr-only">Activity</span></a>
          <a :href="'http://www.tableau.com/uw/cohort/' + row.item.id" :title="'View cohort ' + row.item.name + ' in Tableau'"><i class="fas fa-external-link-alt" /><span class="sr-only">View cohort in Tableau</span></a>
          <a :href="'/cohort/' + row.item.id" :title="'Assign applications to cohort ' + row.item.name">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to cohort ' + row.item.name" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
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
        :items="majors"
        :fields="majorFields"
      >
        <template v-slot:cell(actions)="row">
          <a :href="'/log/' + row.item.id" :title="'Activity for major ' + row.item.name"><i class="far fa-clock" /><span class="sr-only">Activity</span></a>
          <a :href="'/major/' + row.item.id" :title="'Assign applications to major ' + row.item.name">Assign</a>
          <b-button size="sm" :title="'Remove all assignments to major' + row.item.name" @click="info(row.item, row.index, $event.target)">
            Reset
          </b-button>
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
          :title="resetModal.title"
          ok-only
          :ok-title="'Reset ' + collectionType"
          :ok-disabled="resetModal.ok_disabled"
          @hide="resetResetModal"
          @ok="submit_reset"
        >
          <form @submit.prevent="handleUpload">
            <div class="aat-modal-container">
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
            key: 'name',
            label: "Cohort #",
            class: "aat-data-cell aat-data-nowrap",
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
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'protected',
            label: 'Protected',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'admit_decision',
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_count',
            class: "aat-data-cell",
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
            key: 'name',
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
            class: "aat-data-cell",
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
            class: "aat-data-cell",
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
      this.load_data();
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      load_data(){
        axios.get(
          '/api/collection/' + this.collectionType.toLowerCase() + "/",
        ).then(response => {
          if(this.collectionType.toLowerCase() === "cohort"){
            this.cohorts = response.data;
          } else if (this.collectionType.toLowerCase() === "major"){
            this.majors = response.data;
          }
        });
      },
      info(item, index, button) {
        this.resetModal.title = `Reset ${this.collectionType}`;
        this.resetModal.itemId = `${item.id}`;
        this.resetModal.protect = `${item.protect}`;
        this.$root.$emit('bv::show::modal', this.resetModal.id, button);
      },
      resetResetModal() {
        this.resetModal.title = '';
        this.resetModal.content = '';
        this.checked = false;
        this.resetModal.ok_disabled = true;
      },
      submit_reset(){

        axios.delete(
          '/api/collection/' +
            this.$props.collectionType.toLowerCase() +
            "/" +
            this.resetModal.itemId,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            },
            data: {comment: this.comment}
          },
        );
        this.resetResetModal();
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
