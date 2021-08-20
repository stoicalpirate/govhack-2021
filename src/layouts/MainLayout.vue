<template>
  <div>
    <NavBar />
    <div :class="$style.container">
      <b-container fluid="md">
        <slot />
      </b-container>
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from "../components/NavBar"
import Footer from "../components/Footer"
export default {
  name: "Layout",
  components: { NavBar, Footer }
}
</script>

<style lang="css" module>
.container {
  min-width: 25rem;
  max-width: 90rem;
  min-height: 100vh;
  margin: 0 auto;
  margin-top: 120px;
  margin-bottom: 60px;
}
</style>