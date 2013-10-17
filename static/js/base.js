$(function() {
    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }

    $("button#login").click(function() {
        var $username = $("#username").val();
        var $password = $("#password").val();
        if ($username == "") {
            $(".error").text("用户名不能为空");
        } else if ($password == "") {
            $(".error").text("密码不能为空");
        } else {
            var $form = $("#login-form");

            // login
            $.post("/admin/login", $form.serialize())
                .done(function(data) {
                    if (data.status == false) {
                        $(".error").text(data.err_msg);
                    } else {
                        window.location.href = data.go;
                    }
                })
                .fail(function(data) {
                    $(".error").text("服务器内部错误，请查看日志");
                });
        }
    });

    // tag 处理 
    // 从 tags 列表选择 tag
    $(".tag-clouds").on("click", ".ch_tag", function() {
        console.log($(this).text());
        var tags = $(".tag");
        var flag = false;
        for (var i=0; i < tags.length; i++) {
            if (tags.eq(i).text().toLowerCase() == $(this).text()) {
                flag = true;
                return true;
            }
        }
        if (flag == false) {
            $(".tag-group").append($('<a class="tag" href="javascript:void(0);">' + $(this).text() + '</a>'));
            console.log("test");
            $(".tag-group").append($('<input name="tag" value="' + $(this).text() + '" readonly />'));
            $(this).remove();
        }
    });

    $("input.add_tag").keypress(function(event) {
        if (event.which == 13) {
            console.log("Enter");
            var tags = $(".tag");
            var flag = false;
            if ($(this).val() == "") {
                return false;
            }
            for (var i=0; i < tags.length; i++) {
                if (tags.eq(i).text() == $(this).val().toLowerCase()) {
                    flag = true;
                    $(this).val("");
                    return false;
                }
            }
            console.log(flag);
            if (flag == false) {
                $(".tag-group").append($('<a class="tag" href="javascript:void(0);">' + $(this).val() + '</a>'));
                $(".tag-group").append($('<input name="tag" value="' + $(this).val() + '" readonly />'));
                $(this).val("");
            }
            return false;
        }
        console.log(event.which);
    });

    // 绑定动态元素的 click
    $(".tag-group").on("click", ".tag", function() {
        console.log($(this).text());
        var ch_tag = $(".ch_tag");
        var flag = false;
        for (var i = 0; i < ch_tag.length; i++) {
            if ($(this).text().toLowerCase() == ch_tag.eq(i).text()) {
                flag = true;
            }
        }
        if (flag == false) {
            ch_tag.parent().append($('<li class="ch_tag"><a href="javascript:void(0);">' + $(this).text() + '</a></li>'));
        }
        $(this).next().remove();
        $(this).remove();
    });
    $(".del_post").click(function() {
        console.log("test");
        var _xsrf = getCookie("_xsrf");
        console.log($(this).data());
        var del_post = $(this);
        $.post("/admin/post/delete/" + del_post.data("post_id"),
             {"_xsrf": _xsrf})
            .done(function(data) {
                console.log(data);
                if (data.status == true) {
                    window.location.href = "/";
                }
            });
    });
    $("window").keypress(function(event) {
        console.log(event.which);
    });
});
