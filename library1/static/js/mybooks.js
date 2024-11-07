const ReadBook = {
    template:`
    <div class="preview">
            <div class="container" align="center">

                <div class="row" align="right">
                    <div class="col-10"><h4>Book Name: {{$route.query.BookName}}</h4></div>
                    <div class="col-2" align="center"><a href="#" class="btn btn-danger">X</a></div>
                </div><br>
                <iframe :src="getPdfUrl" width="100%" height="575px"></iframe>

            </div>
        </div>
    `,
    computed: {
        getPdfUrl() {
            return `../static/extras/${this.$route.query.BookName}.pdf`;
        }
    }
};

const routes = [
    { path: '/read-book', component: ReadBook }
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    el: '#app',
    router
});