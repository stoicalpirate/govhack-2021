<template>
  <div>
    <Layout>

      <div class="mb-5">
        <h1>Profile</h1>
        <br>
      </div>

      <div v-if="isLoading">
        <Loading />
      </div>

      <div v-else >

        <div class="my-5">
          <h4>Here are the topics and people you're currently tracking:</h4>
          <b-row>
            <b-col cols="4">
              <TopicList v-if="topicDataReceived" :sourceData="selectedTopicsData" @topicselected="setDisplayTopic"/>
              <Loading v-if="!topicDataReceived" />
            </b-col>
            <b-col>
              <b-row>
                <b-col>
                  <div v-if="topicDataReceived">
                    <div v-for="topic in selectedTopicsData" :key="topic.name">
                      <LineChart v-if="topic.name == displayTopic" :sourceData="[topic.federal_trend]"/>   
                    </div>
                  </div>
                </b-col>
              </b-row>
              <b-row>
                <b-col>Key speakers...</b-col>
                <b-col>Ranking in your electorate...</b-col>
                <b-col>Your MP on this issue...</b-col>
              </b-row>
              <b-row>
                <b-col>Datasets...</b-col>
              </b-row>
            </b-col>
          </b-row>
        </div>

        <div class="my-5">
          <h4>Here are some other things you might like to track:</h4>
          <TopicList v-if="topicDataReceived" :sourceData="unselectedTopicsData" @topicselected="userFollowTopic"/>
          <Loading v-if="!topicDataReceived" />
        </div>

        <div class="my-5">
          <h4>Suggest a topic:</h4>
          <b-row class="mb-3">
            <b-col>
              <b-form>
                <b-form-group
                  id="newtopic-group"
                  label="Topic"
                  label-for="newtopic"
                  label-class="font-weight-bold"
                  invalid-feedback="Enter between 1 and 255 characters"
                  :state="newtopicState"
                  class="mb-3"
                >
                  <b-form-input
                    id="newtopic"
                    v-model="newtopic"
                    :state="newtopicState"
                    type="text"
                    trim
                  />
                </b-form-group>
                <b-button
                  @click="upsertNewtopic"
                  variant="success"
                  class="my-2"
                >
                  <span v-if="upsertNewtopicLoading">
                    <b-spinner small variant="light"> </b-spinner>
                  </span>
                  Submit
                </b-button>
              </b-form>
            </b-col>
            <b-col></b-col>
          </b-row>



        </div>

      </div>

    </Layout>
  </div>
</template>

<script>
import Layout from '../layouts/MainLayout'
import Loading from '../components/Loading'
import TopicList from '../components/TopicList.vue'
import LineChart from '../components/LineChart.vue'

export default {
  page: {
    title: "Profile",
  },
  components: { Layout, Loading, TopicList, LineChart },
  data() {
    return {
      isLoading: false,
      topicDataReceived: false,
      selectedTopicsData: [],
      unselectedTopicsData: [],
      displayTopic: "",
      userFollowTopicLoading: false,
      newtopic: "",
      upsertNewtopicLoading: false
    }
  },
  computed: {
    newtopicState() {
      if (this.newtopic.length > 255) {
        return false
      } else if (this.newtopic.length > 0) {
        return true
      } else {
        return null
      }
    }
  },
  mounted() {
    this.getTopicData()
  },
  methods: {
    async getTopicData() {
      this.$http
        .get("/api/user/topicdata")
        .then((response) => {
          this.selectedTopicsData = response.data.selected_topics
          this.unselectedTopicsData = response.data.unselected_topics
          this.displayTopic = this.selectedTopicsData[0].name
          this.topicDataReceived = true
        })
        .catch((error) => {
          console.log(error)
          this.topicDataReceived = true
        })
    },
    setDisplayTopic(topic) {
      this.displayTopic = topic.name
    },
    async userFollowTopic(topic) {
      this.userFollowTopicLoading = true
      const formData = new FormData()
      formData.append("selected_topic", topic)
      this.$http
        .post("/api/user/followtopic", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
        })
        .then(() => {
          console.log("Topic is now being followed.")
          this.userFollowTopicLoading = false
        })
        .catch((error) => {
          console.log(error)
          this.userFollowTopicLoading = false
        })
    },
    async upsertNewtopic() {
      this.upsertNewtopicLoading = true
      const formData = new FormData()
      formData.append("new_topic", this.newtopic)
      this.$http
        .post("api/user/newtopic", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
        })
        .then(() => {
          this.upsertNewtopicLoading = false
        })
        .catch((error) => {
          console.log(error)
          this.upsertNewtopicLoading = false
        })
    }
  }
}
</script>