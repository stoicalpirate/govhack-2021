<template>
  <div>
    <Layout>

      <div class="mb-5">
        <h1>Welcome to SMRT PIE</h1>
        <h4>Smart Public Indexes of Engagement</h4>
        <h5>Our mission is to make government more accessible.</h5>
        <br>
      </div>

      <div class="my-4">
        <h3>TopicFlow</h3>
        <h5>Today's topics minute-by-minute.</h5>
        <StackedBarChart v-if="chartDataReceived" :sourceData="topicflowData"/>
        <Loading v-if="!chartDataReceived" />
      </div>

      <div class="my-4">
        <h3>WordCloud</h3>
        <h5>Most-used words in parliament today.</h5>
        <WordCloud v-if="chartDataReceived" :sourceData="wordcloudData"/>
        <Loading v-if="!chartDataReceived" />
      </div>

      <div class="my-4">
        <h3>SpeakerTime</h3>
        <h5>Politicians who've spoken the most today.</h5>
        <HorizontalBarChart v-if="chartDataReceived" :sourceData="speakertimeData"/>
        <Loading v-if="!chartDataReceived" />
      </div>

      <br><br>
      <!--
      <h3 class="mb-2">Ping the API to check that it's functional:</h3>
      <b-button variant="success" @click="basicApiCall" class="my-2">Ping API</b-button>
      <br>
      <p>API response: {{ message }}</p>
      <br><br>

      <h3 class="mb-2">Check this app can read the user's information after logging in:</h3>
      <b-button variant="success" @click="getUserInfo" class="my-2">Check User Info</b-button>
      <p>User info: {{ printableUserInfo }}</p>
      <br><br>

      <h3 class="mb-2">Check the API can read the user's ID:</h3>
      <b-button variant="success" @click="authorizedPingToApi" class="my-2">Send auth to API</b-button>
      <p>User ID read by API: {{ authConfirmed }}</p>
      <br><br>

      <h3 class="mb-2">Check we can write to the database then read from the database:</h3>
      <b-row class="mb-3">
        <b-col>
          <b-form>
            <b-form-group
              id="key-data-group"
              label="Key"
              label-for="key-data"
              label-class="font-weight-bold"
              invalid-feedback="Enter between 1 and 255 characters"
              :state="keyDataState"
              class="mb-3"
            >
              <b-form-input
                id="key-data"
                v-model="keyData"
                :state="keyDataState"
                type="text"
                trim
              />
            </b-form-group>
            <b-form-group
              id="value-data-group"
              label="Value"
              label-for="value-data"
              label-class="font-weight-bold"
              invalid-feedback="Enter between 1 and 255 characters"
              :state="valueDataState"
              class="mb-3 "
            >
              <b-form-input
                id="value-data"
                v-model="valueData"
                :state="valueDataState"
                type="text"
                trim
              />
            </b-form-group>
            <b-button
              @click="upsertUserRecord"
              variant="success"
              :disabled="upsertButtonDisabled"
              class="my-2"
            >
              <span v-if="upsertLoading">
                <b-spinner small variant="light"> </b-spinner>
              </span>
              Update user info in database
            </b-button>
          </b-form>
        </b-col>
        <b-col></b-col>
      </b-row>
      <p>Updated database record: {{ dbUserRecord }}</p>
      <br><br>
      -->
    </Layout>
  </div>
</template>

<script>
import Layout from '../layouts/MainLayout'
import Loading from '../components/Loading.vue'
import StackedBarChart from '../components/StackedBarChart.vue'
import WordCloud from '../components/WordCloud.vue'
import HorizontalBarChart from '../components/HorizontalBarChart.vue'

export default {
  page: {
    title: "Home",
  },
  components: {
    Layout,
    Loading,
    StackedBarChart,
    WordCloud,
    HorizontalBarChart
  },
  data() {
    return {
      message: "",
      userInfo: Object,
      authConfirmed: "",
      dbUserRecord: {},
      keyData: "",
      valueData: "",
      upsertLoading: false,
      chartDataReceived: false,
      topicflowData: {},
      wordcloudData: {},
      speakertimeData: {}
    };
  },
  computed: {
    printableUserInfo() {
      return JSON.stringify(this.userInfo)
    },
    keyDataState() {
      if (this.keyData.length > 255) {
        return false
      } else if (this.keyData.length > 0) {
        return true
      } else {
        return null
      }
    },
    valueDataState() {
      if (this.valueData.length > 255) {
        return false
      } else if (this.valueData.length > 0) {
        return true
      } else {
        return null
      }
    }
  },
  mounted() {
    this.getChartData()
  },
  methods: {
    async basicApiCall() {
      if (!this.$store.state.loggedIn) {
        this.message = "failed! Are you logged in?"
      } else {
        const { text } = await (await fetch("/api/message/ping")).json()
        this.message = text
      }
    },
    async getUserInfo() {
      const response = await fetch('/.auth/me');
      const payload = await response.json();
      const { clientPrincipal } = payload;
      this.userInfo = clientPrincipal
    },
    async authorizedPingToApi() {
      if (!this.$store.state.loggedIn) {
        this.message = "failed! Are you logged in?"
      } else {
        const { text } = await (await fetch("/api/user/get-id")).json()
        this.authConfirmed = text
      }
    },
    async upsertUserRecord() {
      this.upsertLoading = true
      if (!this.$store.state.loggedIn) {
        this.upsertLoading = false
        this.message = "failed! Are you logged in?"
      } else {
        const formData = new FormData()
        formData.append("key_data", this.keyData)
        formData.append("value_data", this.valueData)
        this.$http
          .post("/api/user/upsert-user", formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
          })
        .then((response) => {
          this.upsertLoading = false
          this.dbUserRecord = response.data
          console.log(this.dbUserRecord)
          this.keyData = ""
          this.valueData = "" 
        })
        .catch((error) => {
          this.dbUserRecord = "error!"
          console.log(error)
          this.upsertLoading = false
        })
      }
    },
    async getChartData() {
      this.$http
        .get("/api/message/chartdata")
        .then((response) => {
          this.topicflowData = response.data.topicflow
          this.wordcloudData = response.data.wordcloud
          this.speakertimeData = response.data.speakertime
          this.chartDataReceived = true
        })
        .catch((error) => {
          console.log(error)
          this.chartDataReceived = true
        })
    }
  }
};
</script>
