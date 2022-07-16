# def executor(self, stmt):
    #     result = self.session.execute(stmt)
    #     for user_obj in result.scalars().all():
    #         row_d = {}
    #         attrs = list(user_obj.__dict__.keys())[1:]
    #         attrs.remove('_id')
    #         row_d['_id'] = getattr(user_obj, '_id')
    #         for col in attrs:
    #             if col == "password":
    #                 continue
    #             row_d[col] = getattr(user_obj, col)
    #         print(row_d)