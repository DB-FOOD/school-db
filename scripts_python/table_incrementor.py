def populate_roles_table(roles):
    """
    Populates the roles table from rovided list.
    """
    sql = ''
    for role_name in roles:
        sql += f"INSERT INTO roles (role) VALUES ('{role_name}');\n"
    return sql