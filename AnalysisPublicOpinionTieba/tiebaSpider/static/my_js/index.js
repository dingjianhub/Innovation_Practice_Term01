$(document).ready(function () {
    // 页面刚开始隐藏搜索结果的部分
    $("#resultSection").hide();

    // id为searchInfo的按钮按下触发searchInfo()方法
    $("#searchInfo").click(function () {
        keyword = $("#keyword").val();
        searchInfo(keyword);
    });

});

// 在按下enter键的时候就搜索
$(document).keyup(function (event) {
    if (event.keyCode == 13) {
        searchInfo($("#keyword").val());
    }
});

function searchInfo(key) {
    // 首先清空result中的内容以便内容填入
    $("#result").empty();
    $.getJSON({
        url: "http://localhost:8080/info?page=1&keyword=杭州电子科技大学",
        success: function (result) {
            // 获取返回的数据中我们需要的部分
            res = result.response.toJSON();
            // 利用for插入每一个结果
            if (res.length) {
                for (i = 0; i < res.length; i++) {
                    // 将返回的结果包装成HTML
                    resultItem =
                        `
                        <div class='col-md-12 mb-4'>
                            <div class='card mb-12 shadow-sm'>
                                <div class='card-body'>
                                    <h5>` +
                        res[i].firstFloorContent +
                        ` <small style='margin-left: 10px'>` +
                        res[i].href +
                        `</small> <small style='margin-left: 10px'>` +
                        res[i].title +
                        `</small></h5>
                                    <p class='text-muted' style='margin-bottom: 0.5em'>` +
                        res[i].href +
                        `</p>
                                    <p class='card-text'>` +
                        res[i].abstract +
                        `</p>
                                </div>
                            </div>
                        </div>
                    `;
                    // 插入HTML到result中
                    $("#result").append(resultItem);
                }

                // 搜索完以后让搜索框移上去，带有动画效果
                $("section.jumbotron").animate({
                    margin: "0"
                });
                // 显示搜索结果的部分
                $("#resultSection").show();
            
            }
        }
    });
}
