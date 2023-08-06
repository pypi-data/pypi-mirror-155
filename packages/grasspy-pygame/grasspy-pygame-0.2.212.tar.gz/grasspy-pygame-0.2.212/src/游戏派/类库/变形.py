导入 pygame
从 游戏派.类库.表层 导入 表层类
类 变形汉化类():

    套路 翻转(自身,表层,水平翻转,垂直翻转)->'表层类':
        '''对表层实现垂直或水平的翻转\n
        参数:<表层>,表层类实例\n
            <水平翻转>,为真时,实例水平翻转\n
            <垂直翻转>,为真时,实例垂直翻转\n
        返回:一个新表层
        '''
        返回 表层类(pygame.transform.flip(表层.surface, 水平翻转,垂直翻转))

    套路 缩放(自身,表层,尺寸, 目标表层 = 空)->'表层类':
        '''对表层实现缩放成指定尺寸\n
        参数:<表层>,表层类实例\n
            <尺寸>,(宽, 高)的元组\n
            <目标表层>,表层类实例\n
        返回:一个新表层
        '''
        如果 目标表层:
            返回 表层类(pygame.transform.scale(表层.surface, 尺寸,目标表层.surface))
        否则:
            返回 表层类(pygame.transform.scale(表层.surface, 尺寸))
    
    套路 旋转(自身,表层,角度)->'表层类':
        '''对表层实现围绕中心的角度旋转\n
        参数:<表层>,表层类实例\n
            <角度>,旋转的角度\n
        返回:一个新表层
        '''
        返回 表层类(pygame.transform.rotate(表层.surface, 角度))

    套路 旋转缩放(自身,表层,角度,缩放比率)->'表层类':
        '''对表层实现旋转与缩放\n
        参数:<表层>,表层类实例\n
             <角度>,旋转的角度\n
             <缩放比率>,旋转的小数比例\n
        返回:一个新表层
        '''
        返回 表层类(pygame.transform.rotozoom(表层.surface, 角度,缩放比率))

    套路 放大2倍(自身,表层,目标表层 = 空)->'表层类':
        '''对表层实现双倍放大\n
        参数:<目标表层>,表层类实例\n
        返回:一个新表层
        '''
        如果 目标表层:
            返回 表层类(pygame.transform.scale2x(表层.surface,目标表层.surface))
        否则:
            返回 表层类(pygame.transform.scale2x(表层.surface))
    
    套路 平滑缩放(自身,表层,尺寸, 目标表层 = 空)->'表层类':
        '''对表层实现平滑缩放成指定尺寸\n
        参数:<表层>,表层类实例\n
             <尺寸>,(宽, 高)的元组\n
             <目标表层>,表层类实例\n
        返回:一个新表层
        '''
        如果 目标表层:
            返回 表层类(pygame.transform.smoothscale(表层.surface, 尺寸,目标表层.surface))
        否则:
            返回 表层类(pygame.transform.smoothscale(表层.surface, 尺寸))

    套路 获取平滑缩放版本(自身)->字符串型:
        '''获取表层实现平滑缩放的过滤版本,'GENERIC', 'MMX', 或 'SSE'\n
        参数:空\n
        返回:版本字符串
        '''
        返回 pygame.transform.get_smoothscale_backend()

    套路 设置平滑缩放版本(自身,版本):
        '''设置表层实现平滑缩放的过滤版本,'GENERIC', 'MMX', 或 'SSE'\n
        参数:版本字符串,'GENERIC', 'MMX', 或 'SSE'\n
        返回:空
        '''
        pygame.transform.set_smoothscale_backend(版本)

    套路 截取(自身,表层,区块)->'表层类':
        '''对表层按区块进行截取,表层只留下区块所在的区域\n
        参数:<表层>,表层类实例\n
            <区块>,区块实例\n
        返回:一个新表层
        '''
        返回 表层类(pygame.transform.chop(表层.surface, 区块.rect))

    套路 查找边缘(自身,表层)->'表层类':
        '''对表层采取拉普算子,去掉背景色,留下边缘线条\n
        参数:<表层>,表层类实例\n
            <区块>,区块实例\n
        返回:一个新表层
        '''
        返回 表层类(pygame.transform.laplacian(表层.surface))

    套路 查找表层平均色(自身,表层列表, 目标表层 = 空, 调色板颜色 = 1)->'表层类':
        '''从多个表层中取得平均色填充的表层,并返回\n
        参数:<表层列表>,表层类实例列表\n
            <目标表层>,表层实例\n
            <调色板颜色>,数字类型\n
        返回:一个新表层
        '''
        _surfaces = 列表型(表层.sprite 取 表层 于 表层列表)
        返回 表层类(pygame.transform.average_surfaces(_surfaces, 目标表层.sprite, 调色板颜色))

    套路 查找平均色(自身,表层, 区块):
        '''从一个表层或区块中取得平均色\n
        参数:<表层>,表层实例\n
            <区块>,区块实例\n
        返回:平均色
        '''
        返回 pygame.transform.average_color(_surfaces, 表层.surface, 区块.rect)