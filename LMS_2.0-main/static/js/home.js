const RequestBook = {
    template:`
    <div class="creationform2">
        <div class="container">
            <h3 align="center">Request Book</h3> <br>
            <form method="POST" action="/request-book">
                <div class="mb-3">
                    <input type="hidden" name="UserID" :value="$route.query.UserID">
                    <input type="hidden" name="BookID" :value="$route.query.BookID">
                    <label for="BookName" class="form-label">Book Name:</label>
                    <input type="text" class="form-control" id="BookName" name="BookName" :value="$route.query.BookName" disabled readonly></input>
                </div>
                <div class="mb-3">
                    <label for="AuthorName" class="form-label">Author Name</label>
                    <input type="text" class="form-control" id="AuthorName" name="authorName" :value="$route.query.Author" disabled readonly></input>
                </div>
                <div class="mb-3">
                    <label for="SectionName" class="form-label">Section Name</label>
                    <input type="text" class="form-control" id="SectionName" name="SectionName" :value="$route.query.SectionName" disabled readonly></input>
                </div>
                <div class="mb-3">
                    <label for="Days" class="form-label">No. of Days:</label>
                    <input type="number" class="form-control" id="Days" name="Days" max="7" min="1">
                    <p style="color:grey;">Cannot be requested for more than 7days.</p>
                </div>
                <br>
                <div class="row" align="center">
                    <div class="col">
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div class="col">
                        <router-link to="/" class="btn btn-danger">Close</router-link>
                    </div>
                </div>
          </form>
        </div>
    </div>
    `
};


const AlreadyRequested = {
    template:`
    <div class="alert1">
            <div class="container" align="center">

                <div class="row" align="right">
                    <div class="col-9"></div>
                    <div class="col-3"><a href="#" class="btn btn-danger">X</a></div>
                </div>
                <br>
                <h1>You have already requested this book.</h1>
                <h4>Please wait for Librarian's approval.</h4>
            </div>
        </div>
    `
};

const GrantedRequest = {
    template:`
    <div class="alert1">
            <div class="container" align="center">

                <div class="row" align="right">
                    <div class="col-9"></div>
                    <div class="col-3"><a href="#" class="btn btn-danger">X</a></div>
                </div>
                <br>
                <h2 style="color: white;">You have already been granted access to this book.</h2>
            </div>
        </div>
    `
};

const MaxRequestLimitReached = {
    template:`
    <div class="alert1">
            <div class="container" align="center">

                <div class="row" align="right">
                    <div class="col-9"></div>
                    <div class="col-3"><a href="#" class="btn btn-danger">X</a></div>
                </div>
                <br>
                <h3>You have reached the maximum limit(5) of book requests.</h3>
                <h5>Please return some books or cancel some pending requests before requesting more.</h5>
            </div>
        </div>
    `
};




const routes = [
    { path: '/request-book', component: RequestBook },
    { path: '/already-requested', component: AlreadyRequested},
    { path: '/granted-request', component: GrantedRequest },
    { path: '/max-request-limit-reached', component: MaxRequestLimitReached }
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    el: '#app',
    router
});



// const app = new Vue({
//     el: '#app',
//     router: new VueRouter({
//         routes: [
//             { path: '/request-book', component: RequestBook },
//             { path: '/already-requested', component: AlreadyRequested },
//             { path: '/granted-request', component: GrantedRequest },
//             { path: '/max-request-limit-reached', component: MaxRequestLimitReached }
//         ]
//     }),
//     data: {
//         searchQuery: '', // Vue.js data property for the search query
//     },
//     computed: {
//         filteredBooks: function () {
//             // Filter the list of books based on the search query
//             return this.sections_with_books.flatMap(section => section.books.filter(book =>
//                 book.book_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
//                 book.author.toLowerCase().includes(this.searchQuery.toLowerCase())
//             ));
//         }
//     }
// });