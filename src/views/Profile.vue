<template>
  <div>
    <Layout>
      <h1>This is the Profile page!</h1>
      <p>This page should only be accessible if the user is logged in.</p>
      <br><br>
      <div v-if="isLoading">
        <Loading />
      </div>
      <div v-else >
        <h3>Put some user data here.</h3>
      </div>
    </Layout>
  </div>
</template>

<script>
import Layout from '../layouts/MainLayout'
import Loading from '../components/Loading'

export default {
  page: {
    title: "Profile",
  },
  components: { Layout, Loading },
  data() {
    return {
      isLoading: false
    }
  },
  created() {

  },
  methods: {

  }
}
</script>