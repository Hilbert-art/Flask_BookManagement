$(function () {
    // 1.首页初始化加载数据
    function fnLoadHomeData(judage) {
        if (judage == "del") {
            $('.del').show();
        } else if (judage == "update") {
            $('.update').show();
        }
    }

    fnLoadHomeData();

    // 1.左侧操作按钮的 交互点击
    var $leftBtns = $('button');
    $leftBtns.click(function () {
        $(this).addClass('leftbtn').parent().siblings().children().removeClass('leftbtn');
    });


    // 查询图书按钮
    $('.checkBook').click(function () {
        $('.booklist').show()
        $('.addlist').hide()
        $('.del').hide()
        $('.update').hide()

    })
    //  增加图书按钮
    $('.addBook').click(function () {
        $('.booklist').hide()
        $('.addlist').show()
    })
    //  删除图书
    $('.delBook').click(function () {
        $('.booklist').show()
        $('.addlist').hide()
        $('.del').show()
        $('.update').hide()
    })
    //  修改图书
    $('.updateBook').click(function () {
        $('.booklist').show()
        $('.addlist').hide()
        $('.del').hide()
        $('.update').show()
    })


    // 监听增加按钮
    $('.add').on('click', function () {
        var addTds = $('.addlist input')
        dict_data = {}
        for (var i = 0; i < (addTds.length - 1); i++) {
            if (i == 0) {
                dict_data.btitle = addTds.eq(i).val()
            } else if (i == 1) {
                dict_data.bauthor = addTds.eq(i).val()
            } else if (i == 2) {
                dict_data.bperson = addTds.eq(i).val()
            } else if (i == 3) {
                dict_data.bpub_date = addTds.eq(i).val()
            } else if (i == 4) {
                dict_data.bread = addTds.eq(i).val()
            }
        }
        if (dict_data.name == "" | dict_data.author == "" | dict_data.hero == "" | dict_data.time == "" | dict_data.read == "") {
            alert('输入内容不能为空!')
            return
        }
        $.post({
            url: "http://127.0.0.1:5000/books/add",
            dataType: "json",
            data: dict_data,
            success: function (dat) {
                alert(dat.data)
                fnLoadHomeData('add')
                window.location.reload()
                // 清空所有 输入框!
                for (var i = 0; i < (addTds.length - 1); i++) {
                    console.log(i)
                    addTds.eq(i).val("")
                }
            }
        })
    })
    // 监听删除按钮
    $('.del').on('click', function () {
        result = $(this).siblings().eq(0).children('input').val()
        $.ajax({
            url: 'http://127.0.0.1:5000/books/delete',
            dataType: 'json',
            type: 'post',
            data: JSON.stringify({id: result}),
            success: function (dat) {
                alert(dat.data)
                $(this).parent().remove()
                console.log($(this))

                fnLoadHomeData('del')

                window.location.reload()
            }
        })

    });
    // 监听修改按钮
    $('.update').on('click', function () {
        var tds = $(this).siblings().children()
        dict_data = {
            "id": tds.eq(0).val(),
            "btitle": tds.eq(1).val(),
            "bauthor": tds.eq(2).val(),
            "bperson": tds.eq(3).val(),
            "bpub_date": tds.eq(4).val(),
            "bread": parseInt(tds.eq(5).val())
        }
        $.ajax({
            url: "http://127.0.0.1:5000/books/update",
            type: "post",
            dataType: 'json',
            data: JSON.stringify(dict_data),
            success: function (dat) {
                alert(dat.data)
                fnLoadHomeData('update')

                window.location.reload()
            }
        })
    })

    $('.idInput').on('focus', function () {
        $(this).blur();
    })
})
    