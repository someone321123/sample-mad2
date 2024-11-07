<template>
  <table>
    <td>
      <form id="ratingForm" style="display:flex" @submit.prevent="submitRating">
        <input type="hidden" name="value" v-model="ratingValue">
        <a href="#" @click="rateSong(1)"><img src="@/assets/STAR.png" width="30px" height="30px" style="margin:0px"></a>
        <a href="#" @click="rateSong(2)"><img src="@/assets/STAR.png" width="30px" height="30px" style="margin:0px"></a>
        <a href="#" @click="rateSong(3)"><img src="@/assets/STAR.png" width="30px" height="30px" style="margin:0px"></a>
        <a href="#" @click="rateSong(4)"><img src="@/assets/STAR.png" width="30px" height="30px" style="margin:0px"></a>
        <a href="#" @click="rateSong(5)"><img src="@/assets/STAR.png" width="30px" height="30px" style="margin:0px"></a>
        <h6 style="padding-top: 10px;">Average Rating: {{ ratings_info.average_rating.toFixed(2) }}</h6>
      </form>
    </td>
  </table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ratingValue: 0,
      ratings_info: {
        average_rating: 0
      },
      username: "", 
    };
  },
  props:["sid"],
  methods: {
    async rateSong(value) {
      this.ratingValue = value;
      await this.submitRating();
    },
    async submitRating() {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/rating-songs`, {
          value: this.ratingValue,
          sid: this.sid,
          id: localStorage.getItem('id')
        });
        this.ratings_info = response.data;
      } catch (error) {
        console.error('Error submitting rating:', error);
        console.log(this.ratingValue, this.sid, localStorage.getItem('id'))
      }
    }
  }
}
</script>


<style> 
@import url("@/assets/style2.css")
</style>